import pickle as pkl

with open('model.pkl', 'rb') as f:
    model = pkl.load(f)


def lambda_handler(event, context):
    user_input = event['body']

    result = model.predict(user_input)

    return {
        'statusCode': 200,
        'body': result
    }
