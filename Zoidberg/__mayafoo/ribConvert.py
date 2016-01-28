import subprocess
def ribToAscii( path ):
    command = [ "C:/Program Files/Pixar/RenderManProServer-18.0/bin/catrib", "-ascii", "-o", path ]
    process = subprocess.Popen( command, stdout=subprocess.PIPE, stdin=None, stderr=subprocess.PIPE )
    output = "\n".join( process.communicate() )
    print output