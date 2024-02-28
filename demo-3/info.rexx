/* REXX */

/* Get address of CVT          */
cvtaddr = get_dec_addr(16)            
/* Get system name at cvt+340 */
zos_name = Strip(Storage(D2x(cvtaddr+340),8))
/* Get address of ECVT */
ecvtaddr = get_dec_addr(cvtaddr+140)
/* Get z/OS version at ECVT+512 */
zos_ver = Strip(Storage(D2x(ecvtaddr+512),2))
/* Get z/OS release at ECVT+514 */
zos_rel = Strip(Storage(D2x(ecvtaddr+514),2))
/* Print our stuff */
say "This is" zos_name "running z/OS V"zos_ver"R"zos_rel

exit

get_dec_addr:
    /* Handy dandy for getting the address stored at
    address :) */
    Parse Arg addr
    hex_addr = d2x(addr)
    stor = Storage(hex_addr,4)
    hex_stor = c2x(stor)
    value = x2d(hex_stor)
    Return value
