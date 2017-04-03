PROJECT DESCRIPTION:
	Goal: Identify the importance of each electro-nodes in reconstructing human speech

	Data Source: Data is from an experiment that clinical doctor electro-nodes in a subject’s cortical surface and subject listens to 2100 human reading sentences. At the same time, recording audio signal and neural signal. 

	Method: 1. Segmenting neural signal by phones in each word in every sentence
			2. Extract features from the segmented neural signal(ecog)
			3. Doing classification on phones by regression on features extracted from neueral signal 
			4. Identify the most effective electro-nodes based on classfication error rate.


BUILD WITH:
	Data Manipulation & IO: pandas; numpy; h5py; pickle 
	Parallel Computing: multiprocessing; joblib; functools
	Visulization: matplotlib, time
	Modeling: scikit-learn
	

HOW TO USE:
	Environment(IDE): Spyder

	Steps:
		1. open Spyder
		2. click "Projects" in the menu
		3. then "Open Project..."
		4. go to this README.txt directory
		5. click choose


CODE STRUCTRE:
	-main.py (user interface)
	-load.py (load all the data)
	-function/DataManipulation.py (raw data scaling)
			  SentenceSegmentation.py (ecog data segmentation by phones)
			  FeatureGeneration.py (create features from segmented ecog data)
		      Visualization.py (dimension reduced data visualization)
			  Prediction.py () (compared the classification performance)
			  util.py (utility functions)


ATTENTION:
	(1) the original data set is fairly large with 2.1GB, here is just very small part of data. Therefore, the visualization and classification performance is not very interesting.
	(2) If the size of dataset is increasing more, distributed computation(Hadoop/Spark) would be the next step



