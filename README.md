# ShutterIsland

Steps taken to retrain the Inception V3 neural network on a Genomic Island dataset. 

1- Call the PATRIC Compare Region service through: 

curl --max-time 300 --data-binary '{\"method\": \"SEED.compare\_regions\_for\_peg\", \"params\": [\"$peg\", 5000, 20, \"pgfam\", \"representative+reference\"], \"id\": 1}' https://p3.theseed.org/services/tf2\_compare\_region"

Where $peg is the query gene of interest. Repeat this call for all pegs of interest and place all the output jsons in one folder (let's call it input\_jsons). 

2- Run the program JsonToCoordinates.py with <input\_jsons> as input to parse the JSON files into a different format to be used by the image generating software. The resulting file will be xyc.txt

3- Compile and run the Java program CoordsToJpg.java which will covert the coordinate file into images. 

4- Split your images into the appropriate classes, then follow the tutorial on:

https://www.tensorflow.org/hub/tutorials/image\_retraining

To re-train the neural network on your own dataset, and test the re-trained model on new images.

The file manualpegtopgf.tab is used to build a dictionary mapping each peg to its corresponding pgf in the reference genome dataset used. That is consequently used to color the arrows accordingly. 
-- 

The reference genomes we used are listed in the file 34\_genomes.pdf
