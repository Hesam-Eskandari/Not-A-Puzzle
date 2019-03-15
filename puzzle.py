from cv2 import waitKey, imshow, destroyAllWindows, line, FONT_HERSHEY_SIMPLEX, putText, circle
from cv2 import namedWindow, setMouseCallback, VideoWriter, EVENT_FLAG_LBUTTON
from numpy import shape, array, ones, zeros
from random import sample, randint
from numpy import sum as np_sum

def rectangle(ground,x_c,y_c,width,thick,fill,color):
    points = [[x_c-width/2,y_c-width/2],[x_c+width/2,y_c-width/2],
              [x_c+width/2,y_c+width/2],[x_c-width/2,y_c+width/2]]
    for ind in [-1,0,1,2]:
        line(ground,(points[ind][0],points[ind][1]),(points[ind+1][0],points[ind+1][1]),color,thick)
    if width <=2 or fill == False:
        return ground
    else:
        return rectangle(ground,x_c,y_c, width-4,thick,fill, color)
    
def move(ground,block,pose1,pose2,velocity,wiper,width):
    if pose1[0] == pose2[0] and pose1[1] == pose2[1]:
        return ground
    else:
        if pose1[0] == pose2[0]:
            if pose1[1] < pose2[1]:
                if ground[pose1[1],pose1[0],0]==255:
                    ground[pose1[1]-width//2:pose1[1]-width//2+velocity,pose1[0]-width//2:pose1[0]+width//2,1:]=wiper
                elif ground[pose1[1],pose1[0],1]==255:
                    ground[pose1[1]-width//2:pose1[1]-width//2+velocity,pose1[0]-width//2:pose1[0]+width//2,[0,2]]=wiper
                elif ground[pose1[1],pose1[0],2]==255:
                    ground[pose1[1]-width//2:pose1[1]-width//2+velocity,pose1[0]-width//2:pose1[0]+width//2,:2]=wiper
                pose1[1]+=velocity
            elif pose1[1] > pose2[1]:
                if ground[pose1[1],pose1[0],0]==255:
                    ground[pose1[1]+width//2-velocity:pose1[1]+width//2,pose1[0]-width//2:pose1[0]+width//2,1:]=wiper
                elif ground[pose1[1],pose1[0],1]==255:
                    ground[pose1[1]+width//2-velocity:pose1[1]+width//2,pose1[0]-width//2:pose1[0]+width//2,[0,2]]=wiper
                elif ground[pose1[1],pose1[0],2]==255:
                    ground[pose1[1]+width//2-velocity:pose1[1]+width//2,pose1[0]-width//2:pose1[0]+width//2,:2]=wiper
                pose1[1]-=velocity
        else:
            if pose1[0] < pose2[0]:
                if ground[pose1[1],pose1[0],0]==255:
                    ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]-width//2:pose1[0]-width//2+velocity,1:]=wiper
                elif ground[pose1[1],pose1[0],1]==255:
                    ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]-width//2:pose1[0]-width//2+velocity,[0,2]]=wiper
                elif ground[pose1[1],pose1[0],2]==255:
                    ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]-width//2:pose1[0]-width//2+velocity,:2]=wiper
                pose1[0]+= velocity
            elif pose1[0] > pose2[0]:
                if ground[pose1[1],pose1[0],0]==255:
                    ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]+width//2-velocity:pose1[0]+width//2,1:]=wiper
                elif ground[pose1[1],pose1[0],1]==255:
                    ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]+width//2-velocity:pose1[0]+width//2,[0,2]]=wiper
                elif ground[pose1[1],pose1[0],2]==255:
                    ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]+width//2-velocity:pose1[0]+width//2,:2]=wiper
                pose1[0]-= velocity
        out.write(ground)
        imshow('PUZZLE',ground)
        key = waitKey(20//velocity) & 0xFF
        if key == 27:
            return []
        if ground[pose1[1],pose1[0],0]==255:
            ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]-width//2:pose1[0]+width//2,1:]=block
        elif ground[pose1[1],pose1[0],1]==255:
            ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]-width//2:pose1[0]+width//2,[0,2]]=block
        elif ground[pose1[1],pose1[0],2]==255:
            ground[pose1[1]-width//2:pose1[1]+width//2,pose1[0]-width//2:pose1[0]+width//2,:2]=block
        #putText(ground,(pose1[0]+10,pose1[1]-10),FONT_HERSHEY_SIMPLEX,1.0,[0,0,0])
        return move(ground,block,pose1,pose2,velocity,wiper,width)
def left_click(event,x,y,flags,param):
    if event == EVENT_FLAG_LBUTTON and np_sum(ground[y,x,:]) == 255:
        distance=[]
        for item in centers:
            distance.append((item[0]-x)**2+(item[1]-y)**2)
        distance = array(distance)
        
        global target
        target = centers[distance == min(distance)][0]

target = []
global target

namedWindow('PUZZLE')
setMouseCallback('PUZZLE', left_click)
dim = 600
global out
out = VideoWriter('PUZZLE.mp4',4, 50, (dim,dim))
width = dim//5
velocity = 12
block = zeros((width,width,2),'uint8')
#block[:,:,0] = 255
horizontal_wiper = ones((width,velocity,2),'uint8')*255
vertical_wiper = ones((velocity,width,2),'uint8')*255
global ground
ground = ones((dim,dim,3),'uint8')*255
#the border rectangle
rectangle(ground,dim//2-velocity//2,dim//2-velocity//2,(width+velocity+1)*4,3,False,[140,210,180])
#colors to create and move blocks
red, green, blue = [0,1], [0,2], [1,2]
colors = sample(5*([blue]+[green]+[red]),15)
#create centers on ground for the blocks 
global centers
centers = []
empty=[randint(0,3),randint(0,3)]
col,i = 0,0
initiate = randint(1,16)
for row in range(4):
    for column in range(4):
        center = [dim//2+(row-2)*(width+velocity)+width//2,dim//2+(column-2)*(width+velocity)+width//2]
        centers.append(center)
        if i!=initiate and col<16:
            ground[center[1]-width//2:center[1]+width//2,center[0]-width//2:center[0]+width//2,colors[col]]=block
            col+=1
        i+=1

centers=array(centers) 
iterate = 0
while True:
    if target!=[]:
        pose1=target
        try:
            if np_sum(ground[pose1[1]+width,pose1[0],:])==3*255 and pose1[1]+width < dim-width//2:
                distance=[]
                for item in centers:
                    if item[0]!=pose1[0] or item[1]!=pose1[1]:
                        distance.append((item[0]-pose1[0])**2+(item[1]-(pose1[1]+width))**2)
                    else:
                        distance.append(255)
                distance = array(distance)
                pose2 = centers[distance == min(distance)][0]
                wiper = vertical_wiper
        except:
            pass
        try:
            if np_sum(ground[pose1[1]-width,pose1[0],:])==3*255 and pose1[1]-width > width//2:
                distance=[]
                for item in centers:
                    if item[1]!=pose1[0] or item[0]!=pose1[1]:
                        distance.append((item[0]-pose1[0])**2+(item[1]-(pose1[1]-width))**2)
                    else:
                        distance.append(255)
                distance = array(distance)
                pose2 = centers[distance == min(distance)][0]
                wiper = vertical_wiper 
        except:
            pass
        try:
            if np_sum(ground[pose1[1],pose1[0]+width,:])==3*255 and pose1[0]+width < dim-width//2:
                distance=[]
                for item in centers:
                    if item[0]!=pose1[0] or item[1]!=pose1[1]:
                        distance.append((item[0]-(pose1[0]+width))**2+(item[1]-pose1[1])**2)
                    else:
                        distance.append(255)
                distance = array(distance)
                pose2 = centers[distance == min(distance)][0]
                wiper = horizontal_wiper
        except:
            pass
        try:
            if np_sum(ground[pose1[1],pose1[0]-width,:])==3*255 and pose1[0]-width > width//2:
                distance=[]
                for item in centers:
                    if item[0]!=pose1[0] or item[1]!=pose1[1]:
                        distance.append((item[0]-(pose1[0]-width))**2+(item[1]-pose1[1])**2)
                    else:
                        distance.append(255)
                distance = array(distance)
                pose2 = centers[distance == min(distance)][0]
                wiper = horizontal_wiper
        except:
            pass
        try:
            if (pose1[0]-pose2[0])**2+(pose1[1]-pose2[1])**2 > (width+velocity)**2:
                pose2 = pose1
            if np_sum(ground[pose2[1]+10,pose2[0]+10,:])==765:
                move(ground,block,pose1,pose2,velocity,wiper,width)
                
        except:
            pass
        target = []
    iterate+=1
    if iterate%8==0:
        out.write(ground)
    imshow('PUZZLE',ground)
    key = waitKey(1) & 0xFF
    if key == 27:
        break
destroyAllWindows()
out.release()

