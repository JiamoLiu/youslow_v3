import pandas as pd
import os

time = ["15","60"]
mbps = ["1Mbps","2Mbps","3Mbps", "4Mbps", "5Mbps"]

def remove_columns_in_csv(folder_path):
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Drop the first 38 columns
            df.drop(df.columns[:38], axis=1, inplace=True)
            df.drop(['defaultMuted', 'disablePictureInPicture', 'disableRemotePlayback', 'draggable'], axis=1, inplace=True)
            df.drop(['ended', 'isConnected', 'isContentEditable', 'localName'], axis=1, inplace=True)
            df.drop(['loop', 'muted', 'namespaceURI', 'outerHTML'], axis=1, inplace=True)
            df.drop(['outerText', 'ownerDocument', 'parentElement', 'parentNode'], axis=1, inplace=True)
            df.drop(['played', 'playsInline', 'preload', 'preservesPitch'], axis=1, inplace=True)
            df.drop(['remote', 'src', 'translate'], axis=1, inplace=True)
            df.drop(['webkitDisplayingFullscreen', 'webkitSupportsFullscreen', 'url'], axis=1, inplace=True)
            df.drop(['defaultPlaybackRate', 'duration', 'extension_loaded_time', "platform", "playbackRate", 'paused'], axis=1, inplace=True)

            # Save the modified file
            df.to_csv(file_path, index=False)
            print(f"Processed {filename}")

# Specify your folder path here
for t in time:
    for m in mbps:
        folder_path = f'data/{t}/{m}/QoE'
        remove_columns_in_csv(folder_path)

# folder_path = 'data/test'
# remove_columns_in_csv(folder_path)
