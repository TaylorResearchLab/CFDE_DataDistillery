DNF4<-array("",c(1,3));
for (i in 1:21) {D <- read.delim(paste("~/Path/4DN Data/Human/",DS[i,1],".txt",sep = "")); 
if (ncol(D)==10) {D <- read.delim(paste("~/Path/4DN Data/Human/",DS[i,1],".txt",sep = ""), header=FALSE)};
if (ncol(D)==12) {D<-D[,c(6:11,4)]} else if (ncol(D)==19) {D<-D[,c(1:6,16)]} else if (ncol(D)==10) {D<-D[,c(1:6,10)]};
U<-array("",c(dim(D)[1],3));
for (j in 1:dim(D)[1]) {U[j,3]  <- paste("4DNL ",D[j,1],":",D[j,2],"-",D[j,3],"_",D[j,4],":",D[j,5],"-",D[j,6],sep = "");
U[j,2]<-"4DN_file_has_loop";U[j,1]<-paste("4DNF ",DS[i,1],sep = "")};DNF4<-rbind(DNF4,U)}
