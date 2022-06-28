import numpy as np
from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.dataset_conversion.utils import generate_dataset_json
from nnunet.paths import nnUNet_raw_data, preprocessing_output_dir
from nnunet.utilities.file_conversions import convert_2d_image_to_nifti
import shutil

if __name__ == '__main__':
    # this is the data folder from the kits21 github repository, see https://github.com/neheller/kits21
    logic_data_dir = '/home/maoyuejingxian/logic/'

    # This script uses the majority voted segmentation as ground truth
    #kits_segmentation_filename = 'aggregated_MAJ_seg.nii.gz'

    # Arbitrary task id. This is just to ensure each dataset ha a unique number. Set this to whatever ([0-999]) you
    # want
    task_id = 501
    task_name = "LogicDie2022"

    foldername = "Task%03.0d_%s" % (task_id, task_name)

    # setting up nnU-Net folders
    target_base = join(nnUNet_raw_data, foldername)

    target_imagesTr = join(target_base, "imagesTr")
    #target_imagesVal = join(target_base, "imagesVal")
    target_labelsTr = join(target_base, "labelsTr")
    target_imagesTs = join(target_base, "imagesTs")
    target_labelsTs = join(target_base, "labelsTs")
    
    maybe_mkdir_p(target_imagesTr)
    maybe_mkdir_p(target_imagesTs)
    maybe_mkdir_p(target_labelsTr)
    maybe_mkdir_p(target_labelsTs)

    train_orig = join(logic_data_dir, "Raw")
    GT_orig = join(logic_data_dir, "Groundtruth")
    test_orig = join(logic_data_dir, "Test", "Raw")
    GT_test_orig = join(logic_data_dir, "Test", "Groundtruth")
    
    print(train_orig, test_orig)
    # convert training set
    cases = sorted([i[:-7] for i in subfiles(train_orig, suffix='.nii.gz', join=False)])
    for i in range(len(cases)):
        c = cases[i]
        data_file = join(train_orig, c+'.nii.gz')

        # before there was the official corrected dataset we did some corrections of our own. These corrections were
        # dropped when the official dataset was revised.
        seg_file = join(GT_orig, c + '.nii.gz')
        if not isfile(seg_file):
            print(i)
            print('raw file : ', data_file)
            print('seg file : ', seg_file)
            exit(-1)

        shutil.copy(data_file, join(target_imagesTr, c + "_0000.nii.gz" ))
        shutil.copy(seg_file, join(target_labelsTr, c + ".nii.gz" )) #'.nii.gz'))

    


    cases = sorted([i[:-7] for i in subfiles(test_orig, suffix='.nii.gz', join=False)])
    for i in  range(len(cases)):
        c = cases[i]
        data_file = join(test_orig, c+'.nii.gz')

        # before there was the official corrected dataset we did some corrections of our own. These corrections were
        # dropped when the official dataset was revised.
        seg_file = join(GT_test_orig, c + '.nii.gz')
        if not isfile(seg_file):
            print(i)
            print('raw file : ', data_file)
            print('seg file : ', seg_file)
            exit(-1)

        shutil.copy(data_file, join(target_imagesTs, c + "_0000.nii.gz"))
        shutil.copy(seg_file, join(target_labelsTs, c + ".nii.gz"))
    

    generate_dataset_json(join(target_base, 'dataset.json'),
                          imagesTr_dir=target_imagesTr,
                          imagesTs_dir=target_imagesTs,
                          modalities = ('CT',),
                          labels = {
                              0: 'background',
                              1: "CuPillar",
                              2: "Solder",
                              3: "Void",
                          },
                          dataset_name = task_name,
                          license='I2R owned',
                          dataset_description='email pahwars@i2r.a-star.edu.sg',
                          dataset_reference='email pahwars@i2r.a-star.edu.sg',
                          dataset_release='0')
