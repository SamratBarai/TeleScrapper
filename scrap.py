import os
import re
from bs4 import BeautifulSoup
import html2text
import requests

# Define Header
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 TelegramBot (like TwitterBot)'
}

#--------------------------------------------#
#         <- HTML Scrapper Functions ->      #
#--------------------------------------------#

#--------------------------------#
# Get HTML content function
def html_to_text(html):
    h = html2text.HTML2Text()
    h.body_width = 0  # Disable line wrapping
    h.ignore_links = True  # Ignore hyperlinks
    h.ignore_emphasis = True  # Ignore bold and italic formatting
    h.ignore_images = True  # Ignore images
    h.protect_links = True  # Protect hyperlinks from being stripped out
    h.unicode_snob = True  # Use Unicode characters instead of ASCII
    h.wrap_links = False  # Disable link wrapping
    h.wrap_lists = False  # Disable list wrapping
    h.decode_errors = 'ignore'  # Ignore Unicode decoding errors

    text = h.handle(html)
    text = re.sub(r'\*+', '', text)  # Remove asterisks
    text = re.sub(r'^[ \t]*[\\`]', '', text, flags=re.MULTILINE)  # Remove leading \ or `
    return text

# Append Image URLs function
def appendImageUrls(link):
    imageUrls = []
    for div in link:
        style = div['style']
        match = re.search(r"background-image:url\('(.*)'\)", style)
        if match:
            bg_image_url = match.group(1)
            imageUrls.append(bg_image_url)
    return imageUrls

# Append Video URLs function
def appendVideoUrls(linkHTML):
    videoUrls = []
    video_tags = linkHTML.find_all('video')
    for video in video_tags:
        src = video.get('src')
        if src:
            videoUrls.append(src)
    return videoUrls
#--------------------------------#

#--------------------------------------------#
#        <- Downloader Functions ->          #
#--------------------------------------------#

#--------------------------------#
# Function to download Images
def downloadIMGs(urlCounter, postFolder, postId, lastIMGPost, mainPath, imageUrls):
    imgCounter = 1

    # Get the image with old link
    oldIMGres = requests.get(lastIMGPost, stream=True)
    oldIMGres.raise_for_status()
    oldIMG = oldIMGres.content

    # Get the image with new link
    newIMGres = requests.get(imageUrls[0], stream=True)
    newIMGres.raise_for_status()
    newIMG = newIMGres.content

    # Skip this url if already downloaded
    if oldIMG == newIMG:
        print("[SYSTEM][EXCEPTION] => Skipping download as the Image files already exist...\n")
        return lastIMGPost
    
    # Download Images
    for url in imageUrls:
        # Define the filepath
        file_path = f"./{mainPath}/{postFolder[urlCounter]}/{postId[urlCounter]}/"

        # Create folders if doesn't exist
        if not os.path.exists(file_path):
            print("[SYSTEM][MANAGER]=> Creating folder...\n")
            os.makedirs(file_path)
        
        # Write Image to file
        response = requests.get(url)
        with open(file_path + str(imgCounter) + ".jpg", 'wb') as f:
            f.write(response.content)
        
        # Finish messege
        print("[INFO] Downloaded ", imgCounter, " image as ", file_path)
        imgCounter += 1
    
    print("[SYSTEM] Images downloaded successfully!\n")

    # Set last downloaded image
    lastIMGPost = imageUrls[0]
    return lastIMGPost

# Function to download Videos
def downloadVIDs(urlCounter, postFolder, postId, lastVIDPost, mainPath, videoUrls):
    vidCounter = 1

    # Get the image with old link
    oldVIDres = requests.get(lastVIDPost, stream=True)
    oldVIDres.raise_for_status()
    oldVID = oldVIDres.content

    # Get the image with new link
    newVIDres = requests.get(videoUrls[0], stream=True)
    newVIDres.raise_for_status()
    newVID = newVIDres.content

    # Skip this url if already downloaded
    if oldVID == newVID:
        print("[SYSTEM][EXCEPTION] :( => Skipping download as the VIDEO files already exist...\n")
        return lastVIDPost
    
    # Download Videos
    for url in videoUrls:
        # Define the filepath
        file_path = f"./{mainPath}/{postFolder[urlCounter]}/{postId[urlCounter]}/"

        # Create folders if doesn't exist
        if not os.path.exists(file_path):
            print("[SYSTEM][MANAGER] => Creating folder...")
            os.makedirs(file_path)
        
        # Write video stream to file
        response = requests.get(url)
        with open(file_path + str(vidCounter) + ".mp4", 'wb') as f:
            f.write(response.content)

        # Finish messege
        print("[INFO] Downloaded ", vidCounter, " image as ", file_path)
        vidCounter += 1

    print("[SYSTEM] Videos downloaded successfully!")

    # Set last downloaded video
    lastVIDPost = videoUrls[0]
    return lastVIDPost
#--------------------------------#

#--------------------------------------------#
#          <- Main Functions ->              #
#--------------------------------------------#

#--------------------------------#
# Main function
def main(urls, mainFolder):
    # Define variables
    urlList = []

    lastIMGPost = ""
    lastVIDPost = ""
    lastIMGPostURL = "https://picsum.photos/200"
    lastVIDPostURL = ""

    postFolders = []
    postIds = []
    urlCounter = 0

    # Find url ids
    for url in urls:
        postFolders.append(url.split('/')[-2])
        postIds.append(url.split('/')[-1])
        urlList.append(url + "?embed=1&mode=tme")
    
    # Find and save media urls
    for link in urlList:
        print("\n[SYSTEM] => Proccessing: ", link, "\n")

        # Find HTML content
        linkReq = requests.get(url=link,headers=headers); linkReq.raise_for_status()
        linkHTML = BeautifulSoup(linkReq.text, 'html.parser')
        # content = html_to_text(str(linkHTML.find('div', {'class': 'tgme_widget_message_text js-message_text', 'dir': 'auto'})))
        # author = html_to_text(str(linkHTML.find('div', {'class': 'tgme_widget_message_author accent_color'}).find('a', {'class': 'tgme_widget_message_owner_name'}).find('span', {'dir': 'auto'})))
        
        # -------------- #
        imgCt = linkHTML.findAll('a', {'class': 'tgme_widget_message_photo_wrap'})
        vidCount = linkHTML.findAll('div', {'class': 'tgme_widget_message_video_wrap'}) 
        # -------------- #

        # Check if the media count is 0
        if len(imgCt) > 0 or len(vidCount) > 0:
            # Append image and video URLs
            imageUrls = appendImageUrls(imgCt)
            videoUrls = appendVideoUrls(linkHTML)

            # Download media
            if len(imageUrls) > 0:
                lastIMGPost = lastIMGPostURL
                lastIMGPostURL = downloadIMGs(urlCounter, postFolders, postIds, lastIMGPost, mainFolder, imageUrls)
            if len(videoUrls) > 0:
                lastVIDPost = lastVIDPostURL
                lastVIDPostURL = downloadVIDs(urlCounter, postFolders, postIds, lastVIDPost, mainFolder,  videoUrls)
        else:
            print("[SYSTEM][EXCEPTION] => Found no media!")
            continue
        urlCounter += 1
            
    print("[SYSTEM] :) => Finished downloading media")

# Main loop
if __name__ == "__main__":
    # Title
    print("\t\t\t\t\t *-------------------------* ")
    print("\t\t\t\t\t | TELEGRAM MEDIA SCRAPPER | ")
    print("\t\t\t\t\t *-------------------------* ")
    print("\t\t\t\t\t             by              ")
    print("\t\t\t\t\t        Samrat Barai         ")
    print("\t\t\t\t\t                             ")

    # Inputs
    inp = input("[SYSTEM][INPUT] => Enter post urls seperated by comma: ")
    mainFolder = input("[SYSTEM][INPUT] => Enter the path for download (Default: content): ")

    # Define the main folder for download
    if mainFolder == "": mainFolder = "content"

    # Find urls and remove extras
    links = inp.split(",")
    for link in links:
        if link.endswith("?single"):
            links[links.index(link)] = link[:-7]
    
    # Print detected urls
    print("[SYSTEM] Detected urls: ", links)

    # Run main function
    main(links, mainFolder)
#--------------------------------#