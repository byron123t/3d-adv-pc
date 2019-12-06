# Rearchitecting Classification Frameworks For Increased Robustness (Generating 3D Adversarial Point Clouds Fork)
Point cloud experiments: [Brian Tang](https://byron123t.github.io/)
In collaboration with: [Varun Chandrasekaran](http://pages.cs.wisc.edu/~chandrasekaran/), [Nicholas Papernot](https://www.papernot.fr/), [Kassem Fawaz](https://kassemfawaz.com/), [Somesh Jha](http://pages.cs.wisc.edu/~jha/), [Xi Wu](http://andrewxiwu.github.io/)

Sample code for our paper, "Rearchitecting Classification Frameworks For Increased Robustness" [arXiv]()

## Requirements
This code is tested with Python 3.5.2
Other required packages can be found in requirements.txt
Sample virtual environment commands:
```
python3 -m venv path_to_environment/
source path_to_environment/bin/activate
pip install -r requirements.txt
```

## Usage
Data processing scripts:
- download_kitti.py -- Downloads the entirety of the [KITTI dataset](http://www.cvlibs.net/datasets/kitti/index.php)
- crop.py -- Crops the RGB images using the annotations and outputs to data/crop/
- pc_crop.py -- Crops the traffic sign point clouds using the annotations and outputs to data/
There are four Python scripts in the root directorty for different attacks:
- train.py -- Train a PointNet model
- evaluate.py -- Evaluate natural accuracy of the model
- perturbation.py -- Adversarial Point Pertubations
- independent.py -- Adversarial Independent Points
- cluster.py -- Adversarial Clusters
- object.py -- Adversarial Objects

The code logics of these four scripts are similar; they attack the victim objects into the specified target class.
The basic usage is `python perturbation.py --target=5`. 

Other parameters can be founded in the script, or run `python perturbation.py -h`. The default parameters are the ones used in the paper.



## Other files
- **gen_initial.py** -- used to generate initial points for adversarial cluster/object. The script uses DBSCAN to cluster the generated critical points.
- critical -- the default directory to dump the generated initial points
- utils/tf_nndistance -- a self-defined tensorlfow op used for Chamfer/Hausdorff distance calculation. Use tf_nndistance_compile.sh to compile the op. The bash code may need modification according to the version and installtion path of CUDA. Note that it should be OK to directly calculate Chamfer/Hausdorff distance with available tf ops instead of tf_nndistance.

## Misc
- Forked from this [repository](https://github.com/xiangchong1/3d-adv-pc)
- We leave integrating other datasets and generalizable code for creating and evaluating hierarchies as future work.
- Please open an issue or contact Brian Tang (byron123t@gmail.com) if there is any question.