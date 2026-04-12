from stratergies import model_strategies

def route_request(model_name:str, input_data:dict):
    try: 
        return model_strategies[model_name](input_data)

    except KeyError:
        raise ValueError(f"Unknown model: {model_name}")