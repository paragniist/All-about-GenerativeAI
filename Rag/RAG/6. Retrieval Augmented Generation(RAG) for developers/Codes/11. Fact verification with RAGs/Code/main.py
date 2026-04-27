from verifier import Verifier

def main():
    verifier = Verifier('./sample_evidence.csv')

    while True:
        claim = input("Enter a claim to verify (or 'quit' to exit): ")
        if claim.lower() == 'quit':
            break

        result, evidence = verifier.verify(claim)
        print(f"\nClaim: '{claim}'")
        print(f"Verification result: {result}")
        print("Supporting evidence: ")
        print(evidence[['evidence', 'label']])
        print("\n")
    
if __name__ == "__main__":
    main()