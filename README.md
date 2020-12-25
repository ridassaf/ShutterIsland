# ShutterIsland

* The file **34_genomes.pdf** lists the genomes used as the testing dataset. 
* The file **manualpegtopfg.tab/** is used to map each gene to its corresponding family. This is used to infer functionality and determine the color of the arrow representing the gene in the generated images. 

<h1> Image Generation </h1> 

The following steps were performed to generate the images:

1. Call the Compare Region Viewer service provided by PATRIC. An example command is:
    curl --max-time 300 --data-binary '{\"method\": \"SEED.compare\_regions\_for\_peg\", \"params\": [\"$peg\", 10000, 20, \"pgfam\", \"representative+reference\"], \"id\": 1}'         https://p3.theseed.org/services/compare\_region"
    Where $peg is the query gene of interest. Repeat this call for all genes/pegs of interest and place all the output jsons in one folder (let's call it **input\_jsons**). 
1. Run the program **JsonToCoordinates.py** with **input\_jsons** as input to parse the JSON files into a different format to be used by the image generating software. The resulting file will be **xyc.txt**, which is the input to **CoordsToJpg.java**. 
1. Compile and run the Java program **CoordsToJpg.java** which will convert the coordinate file into images. 
1. Split your images into the appropriate classes. 

<h1> Transfer Learning </h1> 

We followed the steps outlined in this tutorial to re-train the Inception V3 neural network on our generated images:

https://www.tensorflow.org/hub/tutorials/image_retraining


