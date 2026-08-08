import subprocess

process_stat_cmd = subprocess.Popen(['docker','exec','pg_secure_lab','cat','/proc/1/status'],
                                           stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
filter_kernel_cap = subprocess.run(['grep','-i','CapEff'],
                                            stdin=process_stat_cmd.stdout,check=True,capture_output=True,text=True,timeout=5)
cap_eff_value = filter_kernel_cap.stdout.strip()
print(cap_eff_value)