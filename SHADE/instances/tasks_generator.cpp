#include <iostream>
#include <string>
#include <fstream>
#include <stdlib.h>

using namespace std;

string path="drive/MyDrive/Colab\\ Notebooks";
string instances[]={"Sphere","Elliptic","Rastrigin","Ackley","Rosenbrock","Schwefel"};
string dim[]={"10","30","50"};

int main(int argc,char const *argv[])
{

    //string tarea="/Tarea6/Prueba_30_Correccion";
    string tarea="";

    for(int i=0;i<6;i++){ //for each function
        ofstream tasks;
        tasks.open("tasks_"+instances[i]+".txt");
        for(int k=0;k<3;k++){ //for each dimension
            for(int j = 0; j < 20; j++){ //for each evaluation
                tasks<<" python Evaluation.py"<<" "<<path+tarea+"/dim_"+dim[k]+"/"+instances[i]+"_dim_"+dim[k]+"_out"+to_string(j)+".txt"<<" "<<instances[i]<<" "<<200000<<" "<<100<<" "<<dim[k]<<endl;
            }
        }
        tasks.close();
    }
}

