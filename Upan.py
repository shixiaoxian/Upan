#coding:utf-8
import os,struct,re,fileinput,hashlib,platform,threading
def getdrives(drive_all):
    drives=[]
    drive_all_ = []
    for i in range(65,91):
        vol = chr(i) + ':'
        if os.path.isdir(vol) and vol not in drive_all:
            drive_all_.append(vol)
    for i in range(len(drive_all_)):
        if win32file.GetDriveType(drive_all_[i])==2:
            drives.append(drive_all_[i])
    return drives
def getdrives_linux(sda_list):
    sda_list_n = os.popen("cat /proc/partitions |awk '{ print $4 }'").readlines()[2:]
    upan_list_ = []
    for sd in sda_list_n:
        if sd.split()[0] not in sda_list:
            if len(sd.split()[0]) != 3:
                gua_zai = os.popen("mount | grep '%s'"%sd.split()[0]).readlines()
                if len(gua_zai) != 0:
                    upan_list_.append(gua_zai[0].split(' ')[2])
    return upan_list_
def hash_url(url):
    if not os.path.isfile(url):
        return "update_study"
    else:
        myhash = hashlib.md5()
        f = file(url,'rb')
        while True:
            read_ = f.read(8096)
            if not read_ :
                break
            myhash.update(read_)
        f.close()
        white_study_hash = myhash.hexdigest()
        return white_study_hash
def open_file(path):
    print threading.currentThread().getName()
    file_hash = hash_url(path)
    if file_hash in drive_all:
        fail_.append(path)
    else:
        try:
            file_ = open(path,'r')
        except:
            return 'error'
        read_ = ''.join(file_.read(2048).split())
        while len(read_) > 0:
            c = re.findall('|'.join(list_), read_)
            if len(c) != 0:
                fail_.append(path)
                file_.close()
                break
            read_ = ''.join(file_.read(2048).split())
        file_.close()
        return file_
def print_directory_contents(sPath):
    for sChild in os.listdir(sPath):           
        sChildPath = os.path.join(sPath,sChild)
        if os.path.isdir(sChildPath):
            print_directory_contents(sChildPath)
        else:
            t =threading.Thread(target=open_file,args=(sChildPath,))
            t.start()
if __name__=="__main__":
    list_ = ['加密','密文']
    block_ = ['','']
    drive_all = ['07b181184280e1909724fc0d6c2e9b1d']
    caozuoxitong = platform.system()
    #windows操作系统
    if caozuoxitong == "Windows":
        import win32file
        for i in range(65,91):
            vol = chr(i) + ':'
            if os.path.isdir(vol) and win32file.GetDriveType(vol)==3:
                drive_all.append(vol)
        #while True:
        upan_list = getdrives(drive_all)
        fail_ = []
        for i in upan_list:
            print_directory_contents(i)
        if len(fail_) != 0 :
            print fail_
    #linux操作系统
    elif caozuoxitong == "Linux":
        sda_list_ = os.popen("cat /proc/partitions |awk '{ print $4 }'").readlines()[2:]
        sda_list = []
        for sd in sda_list_:
            sda_list.append(sd.split()[0])
        while True:
            upan_list = getdrives_linux(sda_list)
            fail_ = []
            for i in upan_list:
                print_directory_contents(i)
            if len(fail_) != 0 :
                print fail_
