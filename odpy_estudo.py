import odpy.common as odcommon
import odpy.wellman as odwell
OD_Software_dir = odcommon.getODSoftwareDir()
print("root directory of the Opendtect installation: ", OD_Software_dir)

Bin_sub_dir = odcommon.getBinSubDir()

print("binary sub directory for executables in an OpendTect installation: ", Bin_sub_dir)

OD_Args= odcommon.getODArgs()

print("OpendTect Args", OD_Args)
print("Opendtect survey name:", OD_Args['survey'][0])
print("Is windows?", odcommon.isWin())
print("Is windows?", odcommon.getODSoftwareDir())
print("Well name:", odwell.getNames(reload=True, args=None))
well_name_list = odwell.getNames(reload=True, args=None)
# print("Well information:", odwell.getInfo(well_name_list[0], reload=True, args=None))
# log_list = odwell.getLogNames(well_name_list[0], reload=False, args=None)
# print("Well log list:", log_list)
# print('DT Log: ', odwell.getLog(well_name_list[0], log_list[0], reload=False, args=None))
# gpus = gpuinfo.detect_gpus()
# print(gpus)