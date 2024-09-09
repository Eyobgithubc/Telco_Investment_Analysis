import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def train_and_evaluate_regression(df, features, target):
    """
    Train a linear regression model and evaluate its performance.
    
    Parameters:
    - df: DataFrame containing the data.
    - features: List of feature column names.
    - target: Target column name.
    
    Returns:
    - model: Trained linear regression model.
    - coefficients: DataFrame of feature coefficients.
    - mse: Mean Squared Error of the model.
    - r2: R^2 Score of the model.
    """
    
    # Prepare features and target data
    X = df[features]
    y = df[target]
    
    # Handle any missing values
    X = X.fillna(0)
    y = y.fillna(y.mean())
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Get coefficients
    coefficients = pd.DataFrame(model.coef_, features, columns=['Coefficient'])
    
    return model, coefficients, mse, r2
