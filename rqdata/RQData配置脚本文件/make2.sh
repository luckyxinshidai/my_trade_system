#!/bin/bash
name=license
password=XSphR5wLR8kjIye97VezXJJaPW78p43e-lahmkBmGZ54ozz_godnNQ9YFy7QRLESvbwMIL7SADbq4bc2EWroA1e7lOPpuvmaxh45qsAxd3l1UflUxLeaPt5q6x4ouNfmExSPJDIRtAEHdE0O_5wrFDO4RAzPznonAHcgwqhC9c4=Jsvm2RIul7rDyzeyy8yE_OcVMbJvWI69w5YP5WlPblT8iR-YKONrqY-XJw9kfv1TtQI5LyHGTqLvWTEqSvs0sLt205KAGmNH2_OCL6PoBKAzw4IFRs4OVvAUMrXZavHCmZCXZYr3xwip3DsbfaA2iV_A-Rzcjk-G765RVm26Aww=
host=rqdatad-pro.ricequant.com
port=16011
url=rqdata://${name}:${password}@${host}:${port}
echo "export RQDATAC2_CONF=$url" >> ~/.bash_profile
source ~/.bash_profile
