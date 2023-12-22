import os

data_path = r'C:/Users/scott/desktop/manuscriptproject/code/Generating-Synthetic-Handwritten-Historical-Documents/PyTorch-CycleGAN/datasets/text2kells/train/' # SB old: 'C:/Users/scott/Desktop/ManuscriptProject/Code/Generating-Synthetic-Handwritten-Historical-Documents/HTR_ctc/data/generated/'  # original: '/HOME/pondenka/manuel/CycleGANRD/HTR_ctc/data/generated/'
data_image_names = os.listdir(data_path + 'A') # original & SB old: 'EG-BG-LC')

dataset_path = 'C:/Users/scott/Desktop/ManuscriptProject/Code/Generating-Synthetic-Handwritten-Historical-Documents/CycleGANRD/HTR_ctc/saved_datasets/no/'          # /HOME/pondenka/manuel/CycleGANRD/HTR_ctc/saved_datasets/no/'