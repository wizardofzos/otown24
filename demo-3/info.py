from ctypes import string_at

CVT = string_at(0x10,4).hex()
ecvtLoc = int(CVT,16) + 140
ECVT = string_at(ecvtLoc,4).hex() 


zos_name = string_at(int(CVT,16)+340,8).decode('cp500').strip()
zos_ver  = string_at(int(ECVT,16)+512,2).decode('cp500')
zos_rel  = string_at(int(ECVT,16)+514,2).decode('cp500')


print(f"This is {zos_name} running z/OS V{zos_ver}R{zos_rel}")