# credit_simulator
Credit Simulator for calculating and simulation installment of vehicle

# Run Credit Simulator In Linux
```./credit_simulator``` or ```./credit_simulator file_inputs.txt```

# Run Credit Simulator With Docker
##### Step 1: Get the updated image
```docker pull irenaissance/credit_simulator:master```
##### Step 2: Run the new image with the console based
```docker run -it irenaissance/credit_simulator:master```

###### Or using file_input.txt
```docker run -it irenaissance/credit_simulator:master file_inputs.txt```

# Run UnitTest for Credit Simulator
```python -m unittest credit_simulation\tests\test_credit_simulation.py```

# Rebuild this project with Docker
```docker build -t credit_simulator:${version} .```
