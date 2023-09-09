import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import uvicorn
import base64
import time


## README
# Comments marked with PLOT are followed with code that can be uncommented
# to plot the respective output

# There are 2 types of abnormality detection implemented in this code:
# canny edge and adaptive thresholding
# The former is presently tested to be better so a convenient setting to 
# switch to the latter is not provided, even though easily implementable
# However, the code remnant for the latter is left for testing or future improvement purposes. 

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:4200/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#local
client = MongoClient('mongodb://localhost:27017/')

#server
# mongodb+srv://sebolaprince319:9y7nDs9oG0as1A3u@cluster0.rw0ndtr.mongodb.net/?retryWrites=true&w=majority
client = MongoClient('mongodb+srv://sebolaprince319:9y7nDs9oG0as1A3u@cluster0.rw0ndtr.mongodb.net/?retryWrites=true&w=majority')

db = client['eggs']
collection = db['eggs']

@app.get("/testdb")
async def testdb():
    message = ""
    try:
        client.admin.command('ping')
        message = "Pinged your deployment. You successfully connected to MongoDB! got to : https://cloud.mongodb.com/v2/64fb80a0bbf99942650ec1fc#"
    except Exception as e:
        message = e

    return message

@app.get("/")
async def main():
    message = ''
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        message = "Error: Could not open camera."
        exit()

    start_time = time.time()

    while time.time() - start_time < 3:
        ret, frame = camera.read()
        if not ret:
            message = "Error: Could not capture frame."
            exit()

        cv2.imshow("Captured Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit capturing
            break

    camera.release()
    cv2.destroyAllWindows()  # Close all OpenCV windows
    img_path1 = '../images/eggcandler.jpg'
    img = cv2.imread(img_path1)
    response = getEggData(img)

    try:
        #result = collection.insert_one(response)
        return {"message": f"{message}","response": 12 } if message !="" else response
    except PyMongoError as e:
        return {"message": f"An exception occurred: {e._message}","response": "Data not saved in database" }

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.get("/all")
async def getAll():
    data = []
    result = collection.find()
    for document in result:
        document['_id'] = str(document['_id'])
        data.append(document)

    return data

@app.post("/analyseEgg")
async def analyseEgg(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    return getEggData(image)

def convert_image_to_base64(image):
    # Convert the NumPy array to a byte buffer
    success, buffer = cv2.imencode('.jpg', image)

    if not success:
        print("++++++++++++++++++++++++++ Error encoding image +++++++++++++++++++++++++++")
        exit()

    # Convert the byte buffer to a base64-encoded string
    base64_encoded = base64.b64encode(buffer).decode('utf-8')

    return base64_encoded

def getEggData(image):
    img = image
    # resize for quicker processing 
    img_resized = cv2.resize(img, (900, 900))
    # rgb version
    img_resized_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    # convert to grayscale for processing
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # hough circles
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 50, param1=30, param2=40, minRadius=50, maxRadius=70)
    detected_circles = np.uint16(np.around(circles))
    mask = np.ones_like(img_gray)
    mask[True] = 255

    egg_images = [] # each single egg image
    egg_masks = [] # mask of egg with circle. egg is background due to cv2.circle fill
    egg_coords = [] # coordinates of the egg box. to be used for cv2.rectangle in output
    for x, y, r in detected_circles[0,:]:
        cv2.circle(mask, (x,y), r, (0,255,0), -1)
        egg_images.append(img_gray[y-r:y+r,x-r:x+r])
        egg_masks.append(mask[y-r:y+r,x-r:x+r])
        # coordinates of the box
        x, y, w, h = x-r, y-r, r*2, r*2
        egg_coords.append((x, y, w, h))
    

    # cropping out the egg using the mask
    eggs_cropped = []
    for egg_img, egg_mask in zip(egg_images, egg_masks):
        # change egg to foreground
        egg_mask = cv2.bitwise_not(egg_mask)
        # erode egg mask to cover guaranteed egg region only
        egg_mask = cv2.erode(egg_mask, cv2.getStructuringElement(cv2.MORPH_RECT, (5,5)), iterations=3)
        # apply mask to the egg
        egg_crop = cv2.bitwise_and(egg_img, egg_mask)

        eggs_cropped.append(egg_crop)

    egg_abnormals = []
    eggs_fertilized = []
    img_output = img_resized_rgb.copy()
    for egg_img, egg_mask, egg_coord in zip(eggs_cropped, egg_masks, egg_coords):
        x, y, w, h = egg_coord
        egg_status = analyze_egg(egg_img)
        if egg_status:
            eggs_fertilized.append(egg_status)
            cv2.rectangle(img_output, (x,y),(x+w,y+h), (0,255,0), 2)
            cv2.putText(img_output,'Fertilized', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)

        # use either canny edge or adaptive threshold method to detect abnormalities
        egg_abn = abnormal(egg_img, 1)    

        # change egg to foreground
        egg_mask = cv2.bitwise_not(egg_mask)
        # erode egg mask to cover egg region only
        egg_mask = cv2.erode(egg_mask, cv2.getStructuringElement(cv2.MORPH_RECT, (5,5)), iterations=9)
        # remove outline
        egg_abn = cv2.bitwise_and(egg_abn, egg_mask)

        egg_abnormals.append(egg_abn)

    eggs_fertilized_images = convert_image_to_base64(img_output)

    count = []
    eggs_major_cracked = []
    eggs_minor_cracked = []
    img_output = img_resized_rgb.copy()
    for egg_img, egg_coord in zip(egg_abnormals, egg_coords):
        x, y, w, h = egg_coord
        count.append(np.count_nonzero(egg_img))

        # different count thres for canny and adaptive thres methods
        canny_thres = (70, 20)
        adaptive_thres = (300, 200)
        large_impure, medium_impure = canny_thres # change this depending on canny_thres or adaptive_thres method
        if count[-1] > large_impure:
            eggs_major_cracked.append(egg_img)
            # print("large impurity")
            cv2.rectangle(img_output, (x,y),(x+w,y+h), (255,0,0), 3)
            cv2.putText(img_output,'Major Crack', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
        elif count[-1] > medium_impure:
            eggs_minor_cracked.append(egg_img)
            # print("medium impurity")
            cv2.rectangle(img_output, (x,y),(x+w,y+h), (255,255,0), 3)
            cv2.putText(img_output,'Minor Crack', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
    cracked_eggs = convert_image_to_base64(img_output)

    return {
        "eggsFertilized": eggs_fertilized,
        "crackedEggsImage": cracked_eggs,
        "eggsFertilizedImage": eggs_fertilized_images,
        "eggAbnormals" : len(egg_abnormals),
        "fertilizedEggsCount" : len(eggs_fertilized),
        "eggsMinorCrack": len(eggs_minor_cracked),
        "eggsMajorCrack": len(eggs_major_cracked),
        "total": 29,
    }

def abnormal(egg, style):
    if style == 1:
        # apply canny edge detector to find abnormalities
        egg_abn = cv2.Canny(egg, 150, 100)
    elif style == 2:
        # adaptive thres
        egg_abn = cv2.adaptiveThreshold(egg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 7)
    return egg_abn

def analyze_egg(single_egg):
    # Apply image processing techniques to detect blood vessels or other signs
    # You would need to define the specific techniques based on your hardware and egg type
    
    # Example: Using Canny edge detection to detect blood vessels
    edges = cv2.Canny(single_egg, threshold1=30, threshold2=70)
    
    # Count the number of detected blood vessels
    num_blood_vessels = len(edges[edges > 0])

    # Set a threshold to determine if the egg is fertilized or not
    fertilization_threshold = 500
    is_fertilized = num_blood_vessels >= fertilization_threshold
    
    return is_fertilized

# functions
def plot30(egg_images, title):
    plt.figure(title)
    for index, egg_img in enumerate(egg_images):
        plt.subplot(3, 10 ,index+1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(egg_img, cmap='gray')
        plt.title('{0}'.format(index+1))

pass
if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open camera.")
        exit()
    ret, frame = camera.read()
    if not ret:
        print("Error: Could not capture frame.")
        exit()

    camera.release()

    cv2.imshow("Captured Image", frame)
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close all OpenCV windows


    uvicorn.run(app, host='localhost', port=8000)