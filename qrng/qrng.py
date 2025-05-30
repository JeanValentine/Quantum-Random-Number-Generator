from qiskit import QuantumCircuit, transpile
#transpile is crucial here. It optimizes the quantum circuit for the backend.

from qiskit_aer import Aer
#import the Aer simulator module. Aer is part of the qiskit_aer package. 

from qiskit.visualization import plot_histogram
#This imports the plot_histogram function, specifically designed for visualizing the results of quantum circuits.

import matplotlib.pyplot as plt

# Creating a function to generate quantum random bits
def generate_quantum_random_bits(n_bits=10):
    backend = Aer.get_backend('aer_simulator')
#I used 'qasm_simulator' before, but 'aer_simulator' is more versatile and supports various backends.

    random_bits = []

    for _ in range(n_bits): #loops n_bits times to generate each individual random bit 
        qc = QuantumCircuit(1, 1) #creates a quantum circuit with 1 qubit and 1 classical bit
        qc.h(0)                # Put qubit in superposition
        qc.measure(0, 0)       # Measure qubit

        compiled_circuit = transpile(qc, backend) 
#peforms various transformations and optimizations on the quantum circuit to make it suitable for execution on the specified backend.

        job = backend.run(compiled_circuit, shots=1)
#I used job = execute(qc, backend, shots=1) before, but now I use backend.run(compiled_circuit, shots=1) to run the compiled circuit.
#Instead of the global execute function, I directly run the compiled circuit on the backend.
#This allows me to run the transpiled (optimized) circuit directly and now use the raw qc object.

        result = job.result()
        counts = result.get_counts(qc) #retrives measurement counts 
        bit = list(counts.keys())[0] #extract a single random bit from the counts dictionary
        random_bits.append(bit)

    return ''.join(random_bits) #joins all collected random bits into a single string and returns it 

# Create a function to visualize distribution
def plot_random_distribution(shots=1024): #1024 is a common power of 2 
    qc = QuantumCircuit(1, 1) #create single quantum circuit 
    qc.h(0) #Applies Hadamard gate to the qubit to put it in superposition
    qc.measure(0, 0)

    backend = Aer.get_backend('aer_simulator') 
    compiled_circuit = transpile(qc, backend) #Transpiles the circuit for the backend
    job = backend.run(compiled_circuit, shots=shots) #1024 outcomes 
    result = job.result()
    counts = result.get_counts(qc)

    print("\nDistribution of 0s and 1s over", shots, "shots:")
    print(counts)

    plot_histogram(counts)
    plt.title("Quantum Random Number Distribution")
    plt.show()

# Main entry point
if __name__ == "__main__": #checking if the scropt is being run directly
    n = int(input("How many quantum random bits do you want to generate? ")) 
    bits = generate_quantum_random_bits(n) #calls generate_quantum_random_bits function with user input
    print("\nQuantum Random Bits:", bits)

    visualize = input("\nDo you want to see the distribution histogram? (y/n): ")
    if visualize.lower() == 'y':
        plot_random_distribution()

