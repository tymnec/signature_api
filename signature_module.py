import cv2
from flask import jsonify


def match_signatures(image1_path, image2_path):
    # Read the images
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Use the BFMatcher to find the best matches between the descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Sort the matches based on their distances
    matches = sorted(matches, key=lambda x: x.distance)

    # Set a threshold to consider a match as valid
    threshold = 50

    # Count the number of good matches
    good_matches = [m for m in matches if m.distance < threshold]

    # Calculate the matching score
    matching_score = len(good_matches) / len(matches) * 100

    # You can set a threshold for considering the signatures as similar
    similarity_threshold = 70

    # Check if the matching score is above the similarity threshold
    is_similar = matching_score >= similarity_threshold

    json_dict = {}

    if is_similar:
        json_dict["Answer"] = "Signatures are similar."
    else:
        json_dict["Answer"] = "Signatures are not similar."

    json_dict["Matching Score"] = str(matching_score)

    return jsonify(json_dict)
