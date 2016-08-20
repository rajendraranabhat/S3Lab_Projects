#!/usr/bin/env Rscript

#Read commandline parameters
args = commandArgs(trainingOnly=TRUE)
libFile = args[1]
functionName = args[2]

#Check existence of the function and source the requested file
if(!exists(functionName,mode="function"))
	source(libFile)

#Open stdin
stdin = file("stdin")
open(stdin)

#Read input line by line
while(TRUE){
	#Read one line
	input = readLines(stdin, n=1,ok=TRUE,encoding="UTF-8")
	
	#Check if at the end of the file, if so stop
	if(length(input)==0)
		break

	#Execute function and write result to stdout
	eval(parse(text=paste("write(",functionName,"(input)[[1]]$content,stdout())")))
}
#Close stdin
close(stdin)	
