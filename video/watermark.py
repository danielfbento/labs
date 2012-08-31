import cv
import sys
import glob
import matplotlib.pyplot as plt
from random import *
from numpy import *
from pylab import *


res_frames = []
graph = []
count = 0
n_frame = 0

total_frame_pixel = 0

# Add a frame to the frames to process
def add_frame(frame):
    """ Add a frame to the frames list
    """
    global res_frames 
    if res_frames == None:
        res_frames = []
    res_frames.append(cv.fromarray(frame))

# Get a frame from the frame list at index k
def get_frame(k):
    """ Get a frame from the frame list at index k
    """
    global res_frames
    if res_frames != None and k < len(res_frames):
        return res_frames[k]
    return None

# Return the global frame list size
def get_frames_len():
    """ Return frame list size
    """
    global res_frames
    return len(res_frames)

# Randomize a frame and return it
def get_random_frame():
    """ Get a random frame from the frame list
    """
    global res_frames
    seed()
    p = randint(0,get_frames_len())
    return [get_frame(p),p]

# Empty the frame list to use for each case
def reset_frames():
    """ Empty the frame list
    """
    global res_frames
    res_frames = []

# Gets a submatrix from a matrix, this submatrix
# is obtained using row and column boundings
def get_square(col0,row0,col1,row1,frame):
        """ Gets SubMatrix from Matrix
        """
        # we dont want invalid bounds!
	if (col0 > col1):
                col1, col0 = col0, col1
	if (row0 > row1):
                row1, row0 = row0, row1

	# print "[%d %d, %d %d]" % (row0,col0,row1,col1)

        # if we have more than one row, we select all
        # otherwise we obtain only one row (faster)
	if (row1 > row0):
		matrix = cv.GetRows(frame,row0,row1)
	else:
		matrix = cv.GetRow(frame,row0)
        # same as for rows
	if (col1 > col0):
		matrix = cv.GetCols(matrix,col0,col1)
	else:
		matrix = cv.GetCol(matrix,col0)
	return matrix


def process_frame(x0,y0,x1,y1,frame,result):
	global count
	global n_frame
	global total_frame_pixel
	x_s = int(x0)
	x_e = int(x1)
	y_s = int(y0)
	y_e = int(y1)

	total_pixels = abs(x1-x0) * abs(y1-y0)
	cframe = get_square(x_s,y_s,x_e,y_e,frame)
	tmp    = get_square(x_s,y_s,x_e,y_e,result)

	cdest = cv.CreateImage(cv.GetSize(tmp),8,1)
	bcmp = cv.CreateImage(cv.GetSize(tmp),8,1)

	cv.AbsDiff(cframe,tmp,cdest)
	cv.CmpS(cdest,50,bcmp,cv.CV_CMP_LE)

	nonzero = cv.CountNonZero(bcmp)
	percentage = ((float(nonzero)/float(total_pixels))*100)
	if percentage < 15:
		cv.Set(tmp,cv.Scalar(255,255,255,255))
		return True
	else:
		return frame_divide(x_s,y_s,x_e,y_e,frame,result)
	return False
	
# divide frames in 4 parts
# recursive procedure
def frame_divide(x0,y0,x1,y1,frame,result):

        parts = []

	x_s = int(x0)
	x_e = int(x1)
	y_s = int(y0)
	y_e = int(y1)

        if (abs(x_s - x_e) * abs(y_s - y_e) < 4096):
            return True

        # 4 quadrant
	a = [int(x_s),
             int(y_s),
             int(x_s) + int(math.floor(abs(x_s - x_e)/2)),
             int(y_s) + int(math.floor(abs(y_s - y_e)/2))]
	
        # 1 quadrant
        b = [int(x_s) + int(math.floor(abs(x_s-x_e)/2)),
             int(y_s),
             int(x_e),
             int(y_s) + int(math.floor(abs(y_s - y_e)/2))]
	
        # 3 quadrant
        c = [int(x_s),
             int(y_s) + int(math.floor(abs(y_s - y_e)/2)),
             int(x_s) + int(math.floor(abs(x_s - x_e)/2)),
             int(y_e)]

        # 2 quadrant
	d = [int(x_s) + int(math.floor(abs(x_s - x_e)/2)),
             int(y_s) + int(math.floor(abs(y_s - y_e)/2)),
             int(x_e),
             int(y_e)]

	parts.append(a)
	parts.append(b)
	parts.append(c)
	parts.append(d)

        # run iteratively for each quadrant
	for i in parts:
		xx0 = i[0]
		xx1 = i[2]
		yy0 = i[1]
		yy1 = i[3]

                if (abs(xx0 - xx1) * abs(yy0 - yy1) < 4096):
                    continue
		
                status = process_frame(xx0,yy0,xx1,yy1,frame,result)
		
	return True

# run each image and process
def run_images(dest):
	
	global graph

        graph = []
	
	original = cv.CloneMat(get_random_frame()[0])

        size = cv.GetSize(original)

	added = cv.CreateImage(size,8,1)

	cv.Add(original,original,added)	
	
        for i in range(0,get_frames_len()):	
		if i == get_random_frame()[1]: 
			continue
		process_frame(0,0,size[0],size[1],added,dest)
		added = cv.CloneMat(get_frame(i))
	
        white = cv.CreateImage(size,8,1)
        cv.CmpS(dest,255,white,cv.CV_CMP_NE)
        t = float(size[0]) * float(size[1])
	n = float(cv.CountNonZero(white))
	percent = n / t * 100

	graph.append(percent)
	return dest

# main loop
def main():

	global res_frames
	global graph

        if len(sys.argv) < 4:
            print "usage: %s n_frames n_cases filename \
[filename1 ... filenameN]" % (sys.argv[0])
            return

	print "Starting ", sys.argv[0]
	filenames = sys.argv[3:len(sys.argv)]
	n_frames_to_analyse = int(sys.argv[1])
	n_cases = int(sys.argv[2])

	for filename in filenames:
		print "Reading frames from %s" % filename

		graph = []
		result = []
		
                case = 0

                query_frames = []
               
		capture = cv.CaptureFromFile(filename)
		num_frames = int(cv.GetCaptureProperty(capture, 
                                                cv.CV_CAP_PROP_FRAME_COUNT))

                # query for frames on the input capture
                # for now we are limiting to 4000
                i = 0
                while i <= num_frames and i <= 450:
                    i = i + 1
                    img = cv.QueryFrame(capture)
                    if not img:
                        continue
                    tmp = cv.CreateImage(cv.GetSize(img),8,1)
                    cv.CvtColor(img,tmp,cv.CV_RGB2GRAY)
                    query_frames.append(asarray(cv.GetMat(tmp)))
                # end

                print "Processing CASE ",
		for case in range(0,n_cases):
			print case,
			j = 0
			for j in range(1,n_frames_to_analyse-1):

                                # restart the process
				reset_frames()

                                # randomize the list of frames to analyse
				frames_to_analyse = []
				for k in range(0,len(query_frames)-1):
                                        seed()
                                        frames_to_analyse.append(
                                                    randint(1,
                                                    len(query_frames)-1)
                                                    )
				i = 0
				k = 0

                                # add frames to the work frame list
                                for k in frames_to_analyse:
                                    add_frame(query_frames[k-1])

				if get_frames_len() < 1:
					continue

                                # randomize start frame
				dest=get_frame(j)
                                if dest == None:
                                    graph.append(0)
                                    continue
				dest=run_images(dest)
			result.append(sum(graph)/len(graph))
                # END CASES, PROCESS PLOTING
                print " END"
		r = range(0,n_cases)
		plt.plot(r,result,'k')
		plt.savefig("%s-plot.png" % filename)
		plt.clf()
                print "%s percent: %f" \
                        % (filename, (sum(result)/len(result)))
		
if __name__ == '__main__':
    main()
