

sls function:
1. sls create --template aws-python3 (creates a sls project)
2. sls deploy -v (deploys project to AWS Env)
3. sls deploy -f worker (deploys the function)
4. sls invoke -f worker (invokes a needed function)
5. sls remove ( removes the whole project setup from aws instance)