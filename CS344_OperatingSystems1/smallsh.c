// CS 344: Assignment 3: smallsh
// Andrew Suezaki

/* citations
*  Used example code from 'Exploration: Process API - Executing a New Program' as base code for exec fork source: https://repl.it/@cs344/42execvforklsc
*  Used example code from 'Exploration: Processes and I/O - Example: Redirecting both Stdin and Stdout' as base code for I/O redirection source: https://repl.it/@cs344/54sortViaFilesc
*  Used while loop method for waiting for terminated bg process (line 314) source: https://stackoverflow.com/questions/11322488/how-to-make-sure-that-waitpid-1-stat-wnohang-collect-all-children-process
*  Used example code from 'Exploration: Signal Handling API - Example: Custom Handler for SIGINT' as base code for signal handlers. source: https://repl.it/@cs344/53singal2c
*  Used method to use SIG_IGN on the remaining child bg processes when exiting line(435-436) source: https://stackoverflow.com/questions/18433585/kill-all-child-processes-of-a-parent-but-leave-the-parent-alive
*  Used idea to use sigprocmask for SIGTSTP blocking in child from Piazza @415 and @369 source: https://oregonstate.instructure.com/courses/1798831/external_tools/165861 
*/

// include statements
#include <fcntl.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>

// max argument and input length
#define MAX_ARG 512
#define MAX_IN 2048

// input array to store user command input and argument tokens
char input[MAX_IN];
char *args[MAX_ARG];
// counter for # args inputted
int argcount = 0;
// stores value if process is a bg process
int isbackground = 0;
// stores value if foreground-only mode is active
int isforeground = 0;
// define exit status variable
int exit_status;
// stores value if child terminated by signal ^C
int sigstatus;
// stores signal ^C exit value
int sigexit = 0;
// initialize global SIGINT_action and SIGTSTP_action structs to be empty
struct sigaction SIGINT_action = {0};
struct sigaction SIGTSTP_action = {0};
sigset_t set, oset;
void handle_SIGTSTP(int signo);

// Function to tokenize user input line
char **tokenize(char *inputline){
    // tokenize input using blank space as delim
    char *token = strtok(inputline, " ");
    // variable to increment index for storing tokens into arg array
    int i = 0;
    while (token != NULL && i < MAX_ARG) {
        // place token into arg array
        args[i] = token;
        argcount++;
        // print statement for testing
        // printf("%s\n", token);
        // move to next token
        token = strtok(NULL, " ");
        // increment index
        i++;
    }
    // null terminate arg string for execvp
    args[i] = NULL;
}
/*
* Built-in CD Command
* Function that changes the working directory of smallsh.
*/
void cdcmd(){
    // array to store directory 
    char dir[MAX_IN];
    char *newdir;
    // get current working dir and store in array
    getcwd(dir, sizeof(dir));
    // set newdir = new directory
    newdir = args[1];
    // if a path was not entered, changes to directory specified in HOME environment variable
    if (args[1] == NULL){
        chdir(getenv("HOME"));
    }
    // absolute path handling
    // if current directory string is present in the inputted path string
    else if (strstr(newdir, dir) != NULL){
        // checking if path is valid
        if (chdir(newdir) == -1){
            // prints error message if path is not valid
            printf("Error: path '%s' not found\n", newdir);
            fflush(stdout);
        }
        else {
            // changes dir to inputted path 
            chdir(newdir);
        } 
    }
    // relative path handling
    // adds user inputted path to current working dir array and changes directories
    else {
        // if there is not a / in user input dir
        if (newdir[0] != '/'){
        // add / to end of current directory
        strcat(dir, "/");
        }
        // cat user input dir to current dir
        strcat(dir, newdir);
        // checking if dir is valid
        if (chdir(dir) == -1){
            printf("Error: path '%s' not found\n", dir);
            fflush(stdout);
        }
        else {
            // change to new dir
            chdir(dir);
        }
    }
}

/* 
*  Variable Expansion of $$
*  Function iterates through input line for instances of $$ then converts them to
*  %d and prints the newly formatted string back into the input line
*/ 
void expandvar(){
    // store pid
    int pid = getpid();
    int counter = 0;
    // buffer to temporarily store input line
    char buffer[MAX_IN];
    // iterating through input line 
    for (int i = 0; i < strlen(input); i++){
        // searching for instances of $$
        if ((input[i] == '$') && (input[i+1] == '$')){
            counter++;
            // replacing $$ with %d 
            input[i] = '%';
            input[i+1] = 'd';
        } 
    }
    // print newly formatted input line into buffer
    // replacing %d with pid
    sprintf(buffer, input, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid);
    // print final formatted line into input
    sprintf(input, buffer);
}

// function that prints the exit status
int statuscmd(){
    // if terminated by a signal print proper message
    if (sigstatus == 1){
        printf("terminated by signal %d\n", sigexit);
        fflush(stdout);
    }
    // otherwise print normal exit value message
    else{
        printf("exit value %d\n", exit_status);
        fflush(stdout);
    }
}

/*
* Function to execute commands that aren't built-in.
* see citation at top for base code segments used.
*/ 
void execcmd(){
    // variable to store input/output file
    char *infile = NULL;
    char *outfile = NULL;
    // variables for redirection
    int sourceFD;
    int targetFD; 
    int result;
    int isredirect = 0;
    // blocking ^Z for children
    sigemptyset(&set);
    sigaddset(&set, SIGTSTP);
    sigprocmask(SIG_BLOCK, &set, NULL);
    // searching for input and output files in inputted args
    for (int i=0; i<argcount; i++){
            if (strcmp(args[i], ">") == 0){
                outfile = args[i+1];
                isredirect++;
            }
            if (strcmp(args[i], "<") == 0){
                infile = args[i+1];
                isredirect++;
            }
        }
    // child exit status
    int childStatus;
    // fork a new process
    pid_t spawnPid = fork();
    switch(spawnPid){
        // fork error handling
        case -1:
            perror("fork()\n");
            exit_status = 1;
            exit(1);
            break;
        // child process
        case 0:
            // SIGINT default handler ^C for foreground children only
            if (isbackground == 0 || isforeground == 1){
                SIGINT_action.sa_handler = SIG_DFL;
                sigaction(SIGINT, &SIGINT_action, NULL);
            }
            // handle file redirection
            // if infile was inputted
            if (infile != NULL){
                // opens source file for input redirection
                sourceFD = open(infile, O_RDONLY);
                // source file error handling
                if (sourceFD == -1){
                    printf("cannot open %s for input\n", infile);
                    fflush(stdout);
                    exit_status = 1;
                    exit(1);
                }
                // redirect stdin to source file
                result = dup2(sourceFD, 0);
                // dup2 error handling
                if (result == -1){
                    perror("infile dup2()\n");
                    exit_status = 1;
                    exit(2);
                }
                // close the file descriptor sourceFD when calling exec
                fcntl(sourceFD, F_SETFD, FD_CLOEXEC);
            }
            // if output file inputted
            if (outfile != NULL){
                // open target file for output redirection
                targetFD = open(outfile, O_WRONLY | O_CREAT | O_TRUNC, 0644);
                if (targetFD == -1) {
                    perror("outfile open()");
                    exit_status = 1;
                    exit(1);
                }
                // redirect stdout to target file
                result = dup2(targetFD, 1);
                if (result == -1) {
                    perror("outfile dup2()");
                    exit_status = 1;
                    exit(2);
                }
                // close file descriptor targetFD when calling exec
                fcntl(targetFD, F_SETFD, FD_CLOEXEC);
            }
            // checking if child is a bg process
            if (isbackground == 1 && isforeground == 0){
                // if user didn't redirect stdin
                if (infile == NULL){
                    // redirect stdin to /dev/null
                    sourceFD = open("/dev/null", O_RDONLY);
                    dup2(sourceFD, 0);
                }
                // if user didn't redirect stdout
                if (outfile == NULL){
                    // redirect stdout to /dev/null
                    targetFD = open("/dev/null", O_WRONLY | O_CREAT | O_TRUNC, 0644);
                    dup2(targetFD, 1);
                }
            }
            // if redirected stdin or stdout
            if (isredirect > 0){
                // execute just the command 
                execlp(args[0], args[0], NULL);
            }
            else {
                // otherwise execute command with arg array
                execvp(args[0], args);
            }
            // printf("CHILD(%d) running command %s\n", getpid(), args[0]);
            // prints error if exec returns
            perror(args[0]);
            exit_status = 1;
            exit(1);
            break;
        // parent process
        default:
            // checking if it is a background process and if foreground only mode is not activated
            if (isbackground == 1 && isforeground == 0){
                // print bg process pid
                printf("background pid is %d\n", spawnPid);
                fflush(stdout);
                // continue without waiting for child to finish
                spawnPid = waitpid(spawnPid, &childStatus, WNOHANG);
            }
            // if not, waits for child to finish
            else {
                // reset sig status if new foreground process is run
                sigstatus = 0;
                // waits for child to terminate before returning command line
                spawnPid = waitpid(spawnPid, &childStatus, 0);
                // printf("PARENT(%d): child(%d) terminated. Exiting\n", getpid(), spawnPid);
                // prints message if terminated by ^C signal and sets sig vars to alert status function
                if (WTERMSIG(childStatus) != 0){
                    sigstatus = 1;
                    sigexit = WTERMSIG(childStatus);
                    printf("terminated by signal %d\n", WTERMSIG(childStatus));
                    fflush(stdout);
                }
                // set exit status to child status for status function
                if (WIFEXITED(childStatus)){
                    exit_status = WEXITSTATUS(childStatus);
                }
            }
        // checking for dead child bg process, loop stops once pid returns 0
        while ((spawnPid = waitpid(-1, &childStatus, WNOHANG)) > 0){
            // print message when terminated normally
            if (WIFEXITED(childStatus) != 0){
                printf("background pid %d is done: exit value %d\n", spawnPid, childStatus);
                fflush(stdout);
            }
            // print message when terminated by signal
            if (WIFSIGNALED(childStatus) != 0){
                printf("background pid %d is done: terminated by signal %d\n", spawnPid, WTERMSIG(childStatus));
                fflush(stdout);
            }
            spawnPid = waitpid(-1, &childStatus, WNOHANG);
        }
    }
}

// signal handler for SIGTSTP
void handle_SIGTSTP(int signo){
    // if isforeground is not set, it is starting foreground-only mode
    if (isforeground == 0){
        char* message = "\nEntering foreground-only mode (& is now ignored)\n";
        char* reprompt = ": ";
        // set isforeground to on
        isforeground = 1;
        write(STDOUT_FILENO, message, strlen(message) + 1);
        write(STDOUT_FILENO, reprompt, strlen(reprompt) + 1);
    }
    // otherwise it is exiting foreground-only mode
    else {
        if (isforeground == 1){
            char* message = "\nExiting foreground-only mode\n";
            char* reprompt = ": ";
            // set isforeground to off
            isforeground = 0;
            write(STDOUT_FILENO, message, strlen(message) + 1);
            write(STDOUT_FILENO, reprompt, strlen(reprompt) + 1);
        }
    }
}
/*
*  main() function
*  Initializes signal handlers, uses a while loop to clear 
*  global vars/arrays, then gets and tokenizes user input. 
*  It also handles calls to built-in commands.
*/
int main(void){
    // prints title matching output in assignment specs
    printf("$ smallsh\n");
    fflush(stdout);
    // fill out SIGINT_action struct and set to ignore ^C
    SIGINT_action.sa_handler = SIG_IGN;
    // block catchable signals while running
    sigfillset(&SIGINT_action.sa_mask);
    // no flags set
    SIGINT_action.sa_flags = 0;
    // install signal handler
    sigaction(SIGINT, &SIGINT_action, NULL);
    // initialize/reset SIGTSTP for handling ctrl z after foreground child is done
    SIGTSTP_action.sa_handler = handle_SIGTSTP;
    SIGTSTP_action.sa_flags = SA_RESTART;
    // fill out SIGTSTP_action struct and register handle_SIGTSTP as handler
    sigfillset(&SIGTSTP_action.sa_mask);
    sigaction(SIGTSTP, &SIGTSTP_action, NULL);
    // while loop to reset global vars/arrays and get user input
    while(1){
        // reset input array for new command
        memset(input, '\0', sizeof(input));
        // reset argument array for new command
        memset(args, '\0', sizeof(args));
        // reset global variables
        isbackground = 0;
        argcount = 0;
        // unblock ^Z signal handler
        sigprocmask(SIG_SETMASK, &oset, NULL);
        // prompt user for input
        printf(": ");
        // flush out the output buffers
        fflush(stdout);
        // get input
        fgets(input, MAX_IN, stdin);
        // replace newline at end of fgets input
        input[strlen(input)-1] = '\0';
        // checking for comments and blank lines
        if (input[0] == '\0' || input[0] == '#'){
            // reprompt user if comment or blank line entered
            continue;
        }
        // calls $$ expansion function if $$ is found in the input
        if (strstr(input, "$$") != NULL){
            expandvar();
        }
        // checking if command is a background command
        if (input[strlen(input)-1] == '&'){
            // set background process indicator variable
            isbackground = 1;
            // remove the & for executing
            input[strlen(input)-2] = '\0';
        }
        // split input string into tokens
        tokenize(input);

        // print method for testing purposes
        // printf("\n|%s|\n", args[0]);
        // fflush(stdout);

        // checking for built in commands
        if (strcmp(args[0], "cd") == 0){
            cdcmd();
            continue;
        }
        if (strcmp(args[0], "status") == 0){
            statuscmd();
            continue;
        }
        if (strcmp(args[0], "exit") == 0){
            break;
        }
        execcmd();
        continue;
    }
    // set SIGINT back to default to use on child bg processes
    SIGINT_action.sa_handler = SIG_DFL;
    sigaction(SIGINT, &SIGINT_action, NULL);
    signal(SIGQUIT, SIG_IGN);
    kill(-1*getpid(), SIGQUIT);
    // printf("parent still alive, exiting now..\n");
    return EXIT_SUCCESS; 
}