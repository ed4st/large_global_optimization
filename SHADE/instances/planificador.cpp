#include <iostream>
#include <string>
#include <unistd.h>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <queue>
#include <sys/types.h>
#include <sys/wait.h>

using namespace std;

/*
Ejecutar como:
./planificador machinefile.txt tasksfile.txt
*/

///////////////////////////////////////////////////////////////////

void execute_task(queue <string> *tasks, string machine_available){
    string task = tasks->front();
    execl("/bin/sh","sh","-c",(task).c_str(),(char*) NULL);
}

///////////////////////////////////////////////////////////////////

int main(int argc,char const **argv)
{
    ifstream machinefile,tasksfile;
    string line;
    vector<string> machines;
    queue<string> tasks;
    map<pid_t,string> pids;

    //read files
    if(argc!=3)
    {
        printf("Error en los argumentos\n");
        exit(EXIT_FAILURE);
    }
    else
    {
        machinefile.open(argv[1]);
        tasksfile.open(argv[2]);
    }
    
    //read cores available to use
    while(getline(machinefile,line))
    {
        machines.push_back(line);
    }
    // add tasks to queue
    while(getline(tasksfile,line))
    {
        tasks.push(line);
    }

    machinefile.close();
    tasksfile.close();

    int number_of_process = (machines.size() < tasks.size()) ? machines.size() : tasks.size();

    pid_t id;

    // initialize the executions
    for(int p=0;p<number_of_process;p++)
    {
        id = fork();

        // child process
        if(id==0)
        {   
            execute_task(&tasks,machines[p]);
            exit(0);
        } 
        if(id>0)//parent process
        {
            tasks.pop();
            pids[id]=machines[p];
        }
        else
        {
            cout<<"Error en fork()"<<endl;
        }
        usleep(10000);
    }

    while(tasks.size()>0) // wait for tasks to end
    {
        pid_t pid = waitpid(-1,NULL,0);

        if(pid==-1)
        {
            printf("Error en waitpid\n");
            exit(EXIT_FAILURE);
        }
        if(pid>0)
        {
            //tasks completed
            map<int,string>::iterator it = pids.find(pid);
            string machine_available = pids[pid];
            pids.erase(it);

            id = fork();

            if(id==0) //child process
            {   
                execute_task(&tasks,machine_available);
                exit(0);
            } 
            if(id>0) //parent process
            {
                tasks.pop();
                pids[id]=machine_available;
            }
            else 
            {
                cout<<"Error en fork()"<<endl;
            }
        }
        usleep(10000);
    }
    return 0;
}
