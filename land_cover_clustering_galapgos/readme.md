🌎 **Land Cover Classification and Clustering Project in the Galapagos Islands**

📝 **General Description**

This project includes implementations for land cover classification in the Galapagos Islands using clustering algorithms. The techniques employed include:

🌐 Using Google Earth Engine (GEE) to process and analyze satellite data.

📊 Applying clustering algorithms, such as KMeans, on Sentinel-2 satellite data.

The provided notebooks explore approaches using both cloud-based tools (GEE) and local Python libraries.

📁 **Project Content**

1. 📜 Clustering_land_cover_classification_GEE_Galapagos.ipynb

Purpose: Utilize Google Earth Engine to perform clustering and land cover classification.

Key Technologies:

🌐 Google Earth Engine (GEE).

🗺️ geemap library for interactive visualization of geospatial data.

Highlighted Functions:

☁️ mask_s2_clouds: Custom function to filter clouds in Sentinel-2 images.

2. 🖥️ **Simple_sklearn_cluster_algorithm_Galapgos.ipynb**

Purpose: Apply the KMeans algorithm using locally processed data.

Key Technologies:

🤖 sklearn to implement KMeans.

🖼️ rasterio and osgeo for handling raster data.

📊 matplotlib and numpy for visualization and data manipulation.

⚙️ **Requirements**

To run the notebooks, ensure the following dependencies are installed:

🐍 Python 3.8+

📦 **Required libraries:**

pip install numpy matplotlib sklearn rasterio osgeo geemap earthengine-api

🌐 An account enabled to use Google Earth Engine (required for the first notebook).

▶️ **Execution**

🔄 Clone this repository:

git clone <repository-URL>
cd <repository-name>

🏃‍♂️ **Run the notebooks:**

For the GEE-based notebook, make sure to log in:

earthengine authenticate

Open the .ipynb files in Jupyter Notebook or JupyterLab.

🚀 Follow the instructions in each notebook to reproduce the results.

🎯 **Results**

Land Cover Classification: 🗺️ Classification maps with clusters representing different types of terrain.

Visualizations: 📈 Interactive graphs and maps showing the clustering results.

