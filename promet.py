from paramiko import SSHClient, AutoAddPolicy
import os
import pysftp
import time

hostname = 'pro.cyfronet.pl'
username = 'username'
password = 'password'

# qmmm.sh i qmmm.in muszą być w tym folderze, z parametrami jobname=XXX, qmmm.in PM6, :295
dir = 'dir' # on prometheus
localdir = 'localdir'  # do sftp
keydir = 'keydir'
commands = []
methods = ['AM1', 'RM1', 'DFTB3', 'PM3', 'PM6']
# levels = ['1', '2', '3', '4', '5']
levels = ['4', '5']
samples = ['nonrestrainedbrom', 'nonrestrainedchlor']
qmcharge = [0, -1, -2]
# atoms for QM
atomsC = ["':295'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3 | :308 | :270@NE2,CD2,CG,ND1,CE1,HD2,HD1,HE1,CB,HB2,HB3'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3 | :308 | :270@NE2,CD2,CG,ND1,CE1,HD2,HD1,HE1,CB,HB2,HB3 | :130@CG,HG3,"
          "HG2,CD,OE1,OE2'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3 | :308 | :270@NE2,CD2,CG,ND1,CE1,HD2,HD1,HE1,CB,HB2,HB3 | :130@CG,HG3,"
          "HG2,CD,OE1,OE2 | :36@CB,HB2,HB3,CG,OD1,ND2,HD21,HD22 | :107@CB,HB2,HB3,CG,CD1,HD1,NE1,HE1,CE2,CD2,CE3,HE3,"
          "CZ3,HZ3,CH2,HH2,CZ2,HZ2' "
          ]
waterC = " '308' "
waterB = " '9942' "
atomsB = ["':295'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3 | :9942 | :270@NE2,CD2,CG,ND1,CE1,HD2,HD1,HE1,CB,HB2,HB3'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3 | :9942 | :270@NE2,CD2,CG,ND1,CE1,HD2,HD1,HE1,CB,HB2,HB3 | :130@CG,HG3,"
          "HG2,CD,OE1,OE2'",
          "':295 | :106@OD2,CB,OD1,CG,HB2,HB3 | :9942 | :270@NE2,CD2,CG,ND1,CE1,HD2,HD1,HE1,CB,HB2,HB3 | :130@CG,HG3,"
          "HG2,CD,OE1,OE2 | :36@CB,HB2,HB3,CG,OD1,ND2,HD21,HD22 | :107@CB,HB2,HB3,CG,CD1,HD1,NE1,HE1,CE2,CD2,CE3,HE3,"
          "CZ3,HZ3,CH2,HH2,CZ2,HZ2' "
          ]
client = SSHClient()
client.load_host_keys(keydir)
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect(hostname=hostname, port=22, username=username, password=password)

making directories
for sample in samples:
    makedir1 = 'cd ' + dir + '; mkdir ' + sample
    makedir4 = 'cd ' + dir + sample + '; mkdir QM'
    commands = commands + [makedir1] + [makedir4]
    for level in levels:
        makedir2 = 'cd ' + dir + sample + '/QM' + '; mkdir ' + level
        commands = commands + [makedir2]
        for method in methods:
            makedir3 = 'cd ' + dir + sample + '/QM/' + level + '; mkdir ' + method
            commands = commands + [makedir3]

copying files to all dirs - works
for sample in samples:
    for level in levels:
        for method in methods:
            path = 'cp ' + dir + 'qmmm.sh' + ' ' + dir + sample + '/QM/' + level + '/' + method
            commands = commands + [path]
            path = 'cp ' + dir + 'qmmm.in' + ' ' + dir + sample + '/QM/' + level + '/' + method
            commands = commands + [path]
            path = 'cp ' + dir + 'analiza.sh' + ' ' + dir + sample + '/QM/' + level + '/' + method
            commands = commands + [path]
            if sample == 'nonrestrainedbrom':
                path = 'cp ' + dir + '*B.top' + ' ' + dir + sample + '/QM/' + level + '/' + method + '/top.top'
                commands = commands + [path]
                path = 'cp ' + dir + '*B.crd' + ' ' + dir + sample + '/QM/' + level + '/' + method + '/doQM.crd'
                commands = commands + [path]
                path = 'cp ' + dir + '*B.in' + ' ' + dir + sample + '/QM/' + level + '/' + method + '/analiza.in'
                commands = commands + [path]
            else:
                path = 'cp ' + dir + '*C.top' + ' ' + dir + sample + '/QM/' + level + '/' + method + '/top.top'
                commands = commands + [path]
                path = 'cp ' + dir + '*C.crd' + ' ' + dir + sample + '/QM/' + level + '/' + method + '/doQM.crd'
                commands = commands + [path]
                path = 'cp ' + dir + '*C.in' + ' ' + dir + sample + '/QM/' + level + '/' + method + '/analiza.in'
                commands = commands + [path]

# executing
for element in commands:
    client.exec_command(element)
    stdin, stdout, stderr = client.exec_command(element)
    print(stdout.read().decode())
    print(stderr.read().decode())
commands = []

# rewriting parameters in files via SFTP and downloading data
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection('pro.cyfronet.pl',
                       username=username,
                       password=password,
                       cnopts=cnopts
                       ) as sftp:
    for sample in samples:  # qmmm.sh
        for level in levels:
            for method in methods:
                if sample == 'nonrestrainedbrom':
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.sh', localdir + 'qmmm.sh')
                    with open(localdir + 'qmmm.sh', 'r') as file:
                        filedata = file.read()
                        filedata = filedata.replace('XXX', str('B' + level + method))
                        filedata = filedata.replace(dir, dir + sample + '/QM/' + level + '/' + method)
                        filedata = filedata.replace('#SBATCH --nodes=1', '#SBATCH --nodes=10')
                    with open(localdir + 'qmmm.sh', 'w') as file:
                        file.write(filedata)
                    sftp.put(localdir + 'qmmm.sh',
                             dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.sh')
                    os.remove(localdir + 'qmmm.sh')
                else:
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.sh', localdir + 'qmmm.sh')
                    with open(localdir + 'qmmm.sh', 'r') as file:
                        filedata = file.read()
                        filedata = filedata.replace('XXX', str('C' + level + method))
                        filedata = filedata.replace(dir, dir + sample + '/QM/' + level + '/' + method)
                        filedata = filedata.replace('#SBATCH --nodes=1', '#SBATCH --nodes=10')
                    with open(localdir + 'qmmm.sh', 'w') as file:
                        file.write(filedata)
                    sftp.put(localdir + 'qmmm.sh',
                             dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.sh')
                    os.remove(localdir + 'qmmm.sh')
    for sample in samples:  # analiza.sh
        for level in levels:
            for method in methods:
                sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'analiza.sh', localdir + 'analiza.sh')
                with open(localdir + 'analiza.sh', 'r') as file:
                    filedata = file.read()
                    filedata = filedata.replace(dir, dir + sample + '/QM/' + level + '/' + method)
                with open(localdir + 'analiza.sh', 'w') as file:
                    file.write(filedata)
                sftp.put(localdir + 'analiza.sh',
                         dir + sample + '/QM/' + level + '/' + method + '/' + 'analiza.sh')
                os.remove(localdir + 'analiza.sh')
    for sample in samples:  # qmmm.in
        for level in levels:
            for method in methods:
                if sample == 'nonrestrainedbrom':
                    if level == '1':
                        sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in',
                                 localdir + 'qmmm.in')
                        with open(localdir + 'qmmm.in', 'r') as file:
                            filedata = file.read()
                            filedata = filedata.replace("':295'", (atomsB[int(level) - 1]))
                            filedata = filedata.replace('PM6', method)
                        with open(localdir + 'qmmm.in', 'w') as file:
                            file.write(filedata)
                        sftp.put(localdir + 'qmmm.in',
                                 dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in')
                        os.remove(localdir + 'qmmm.in')
                    if level in ('2', '3'):
                        sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in',
                                 localdir + 'qmmm.in')
                        with open(localdir + 'qmmm.in', 'r') as file:
                            filedata = file.read()
                            filedata = filedata.replace("':295'", (atomsB[int(level) - 1]))
                            filedata = filedata.replace('PM6', method)
                            filedata = filedata.replace('qmcharge=0', 'qmcharge='+str(qmcharge[1]))
                        with open(localdir + 'qmmm.in', 'w') as file:
                            file.write(filedata)
                        sftp.put(localdir + 'qmmm.in',
                                 dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in')
                        os.remove(localdir + 'qmmm.in')
                    if level in ('4', '5'):
                        sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in',
                                 localdir + 'qmmm.in')
                        with open(localdir + 'qmmm.in', 'r') as file:
                            filedata = file.read()
                            filedata = filedata.replace("':295'", (atomsB[int(level) - 1]))
                            filedata = filedata.replace('PM6', method)
                            filedata = filedata.replace('qmcharge=0', 'qmcharge='+str(qmcharge[2]))
                        with open(localdir + 'qmmm.in', 'w') as file:
                            file.write(filedata)
                        sftp.put(localdir + 'qmmm.in',
                                 dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in')
                        os.remove(localdir + 'qmmm.in')
                else:
                    if level in ('1'):
                        sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in',
                                 localdir + 'qmmm.in')
                        with open(localdir + 'qmmm.in', 'r') as file:
                            filedata = file.read()
                            filedata = filedata.replace("':295'", (atomsC[int(level) - 1]))
                            filedata = filedata.replace('PM6', method)
                        with open(localdir + 'qmmm.in', 'w') as file:
                            file.write(filedata)
                        sftp.put(localdir + 'qmmm.in',
                                 dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in')
                        os.remove(localdir + 'qmmm.in')
                    if level in ('2', '3'):
                        sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in',
                                 localdir + 'qmmm.in')
                        with open(localdir + 'qmmm.in', 'r') as file:
                            filedata = file.read()
                            filedata = filedata.replace("':295'", (atomsC[int(level) - 1]))
                            filedata = filedata.replace('PM6', method)
                            filedata = filedata.replace('qmcharge=0', 'qmcharge=' + str(qmcharge[1]))
                        with open(localdir + 'qmmm.in', 'w') as file:
                            file.write(filedata)
                        sftp.put(localdir + 'qmmm.in',
                                 dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in')
                        os.remove(localdir + 'qmmm.in')
                    if level in ('4', '5'):
                        sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in',
                                 localdir + 'qmmm.in')
                        with open(localdir + 'qmmm.in', 'r') as file:
                            filedata = file.read()
                            filedata = filedata.replace("':295'", (atomsC[int(level) - 1]))
                            filedata = filedata.replace('PM6', method)
                            filedata = filedata.replace('qmcharge=0', 'qmcharge=' + str(qmcharge[2]))
                        with open(localdir + 'qmmm.in', 'w') as file:
                            file.write(filedata)
                        sftp.put(localdir + 'qmmm.in',
                                 dir + sample + '/QM/' + level + '/' + method + '/' + 'qmmm.in')
                        os.remove(localdir + 'qmmm.in')

# getting data from server
    for sample in samples:  # analysis
        for level in levels:
            for method in methods:
                if sample == 'nonrestrainedbrom':
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'disCO.dat',
                             localdir + '/1/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'disXNE.dat',
                             localdir + '/2/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'disXND.dat',
                             localdir + '/3/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'angOCX.dat',
                             localdir + '/4/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'angONH.dat',
                             localdir + '/5/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'dihXCCX.dat',
                             localdir + '/6/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_270_130avg.dat',
                             localdir + '/7/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_9942_270avg.dat',
                             localdir + '/8/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_9942_106avg.dat',
                             localdir + '/9/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_36_9942avg.dat',
                             localdir + '/10/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_105_270avg.dat',
                             localdir + '/11/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'rmsd.dat',
                             localdir + '/12/' + 'B' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'rmsf.dat',
                             localdir + '/13/' + 'B' + level + method + '.dat')
                    print('B' + level + method + ' finished')
                else:
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'disCO.dat',
                             localdir + '/1/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'disXNE.dat',
                             localdir + '/2/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'disXND.dat',
                             localdir + '/3/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'angOCX.dat',
                             localdir + '/4/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'angONH.dat',
                             localdir + '/5/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'dihXCCX.dat',
                             localdir + '/6/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_270_130avg.dat',
                             localdir + '/7/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_308_270avg.dat',
                             localdir + '/8/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_308_106avg.dat',
                             localdir + '/9/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_36_308avg.dat',
                             localdir + '/10/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'hbond_105_270avg.dat',
                             localdir + '/11/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'rmsd.dat',
                             localdir + '/12/' + 'C' + level + method + '.dat')
                    sftp.get(dir + sample + '/QM/' + level + '/' + method + '/' + 'rmsf.dat',
                             localdir + '/13/' + 'C' + level + method + '.dat')
                    print('C' + level + method + ' finished')
    for sample in samples:  # analysis prod
        if sample == 'nonrestrainedbrom':
            sftp.get(dir + sample + '/' + 'disCO.dat', localdir + '/1/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'disXND.dat', localdir + '/2/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'disXNE.dat', localdir + '/3/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'angOCX.dat', localdir + '/4/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'angONH.dat', localdir + '/5/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'dihXCCX.dat', localdir + '/6/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_270_130avg.dat', localdir + '/7/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_9942_270avg.dat', localdir + '/8/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_9942_106avg.dat', localdir + '/9/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_36_9942avg.dat', localdir + '/10/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_105_270avg.dat', localdir + '/11/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'rmsd.dat', localdir + '/12/' + 'Bprod.dat')
            sftp.get(dir + sample + '/' + 'rmsf.dat', localdir + '/13/' + 'Bprod.dat')
        else:
            sftp.get(dir + sample + '/' + 'disCO.dat', localdir + '/1/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'disXND.dat', localdir + '/2/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'disXNE.dat', localdir + '/3/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'angOCX.dat', localdir + '/4/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'angONH.dat', localdir + '/5/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'dihXCCX.dat', localdir + '/6/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_270_130avg.dat', localdir + '/7/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_308_270avg.dat', localdir + '/8/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_308_106avg.dat', localdir + '/9/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_36_308avg.dat', localdir + '/10/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'hbond_105_270avg.dat', localdir + '/11/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'rmsd.dat', localdir + '/12/' + 'Cprod.dat')
            sftp.get(dir + sample + '/' + 'rmsf.dat', localdir + '/13/' + 'Cprod.dat')
sftp.close()

# launching jobs
for sample in samples:
    for level in levels:
        for method in methods:
            path = 'cd ' + dir + sample + '/QM/' + level + '/' + method + '; dos2unix qmmm.sh; /net/slurm/releases/production.x86_64/bin/sbatch qmmm.sh' #/net/slurm/releases/production.x86_64/bin/  pierszy source /etc/profile;
            commands = commands + [path]

# executing
for element in commands:
    print(element)
    client.exec_command(element)
    stdin, stdout, stderr = client.exec_command(element)
    print(stdout.read().decode())
    print(stderr.read().decode())
    # time.sleep(5) # do testingu

client.close()
