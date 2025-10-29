import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def analyze_transaction_patterns(df):
    """
    Analyze transaction patterns for unusual behavior
    Expected columns: date, amount, transaction_type, merchant/description
    Returns: dict with anomalies, statistics, and alerts
    """
    results = {
        "total_transactions": len(df),
        "anomalies": [],
        "statistics": {},
        "alerts": [],
        "risk_score": 0.0
    }
    
    if df.empty:
        results["alerts"].append("No transactions to analyze")
        return results
    
    # Ensure amount column exists and is numeric
    if 'amount' not in df.columns:
        results["alerts"].append("Missing 'amount' column")
        return results
    
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])
    
    # Basic statistics
    results["statistics"] = {
        "total_amount": float(df['amount'].sum()),
        "average_amount": float(df['amount'].mean()),
        "median_amount": float(df['amount'].median()),
        "max_amount": float(df['amount'].max()),
        "min_amount": float(df['amount'].min()),
        "std_deviation": float(df['amount'].std())
    }
    
    # 1. Detect unusually large transactions (amount-based anomalies)
    mean_amount = df['amount'].mean()
    std_amount = df['amount'].std()
    threshold = mean_amount + (3 * std_amount)
    
    large_transactions = df[df['amount'] > threshold]
    for idx, row in large_transactions.iterrows():
        results["anomalies"].append({
            "type": "Large Transaction",
            "index": int(idx),
            "amount": float(row['amount']),
            "reason": f"Amount ${row['amount']:.2f} is {((row['amount'] - mean_amount) / std_amount):.1f} standard deviations above mean",
            "severity": "high" if row['amount'] > threshold * 1.5 else "medium"
        })
    
    # 2. Detect round number transactions (potential money laundering indicator)
    round_numbers = df[df['amount'] % 100 == 0]
    if len(round_numbers) > len(df) * 0.3:  # More than 30% are round numbers
        results["alerts"].append(f"High frequency of round number transactions ({len(round_numbers)}/{len(df)})")
    
    # 3. Check for date-based patterns if date column exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        
        if not df.empty:
            # Detect transactions at unusual hours (if time information exists)
            df['hour'] = df['date'].dt.hour
            night_transactions = df[(df['hour'] >= 0) & (df['hour'] <= 5)]
            if len(night_transactions) > 0:
                results["alerts"].append(f"{len(night_transactions)} transactions during night hours (12 AM - 5 AM)")
            
            # Detect rapid succession transactions
            df_sorted = df.sort_values('date')
            time_diffs = df_sorted['date'].diff()
            rapid_transactions = time_diffs[time_diffs < timedelta(minutes=1)]
            if len(rapid_transactions) > 0:
                results["alerts"].append(f"{len(rapid_transactions)} transactions within 1 minute of each other")
            
            # Daily transaction frequency
            daily_counts = df.groupby(df['date'].dt.date).size()
            avg_daily = daily_counts.mean()
            if daily_counts.max() > avg_daily * 3:
                results["alerts"].append(f"Unusual daily transaction frequency detected (max: {daily_counts.max()}, avg: {avg_daily:.1f})")
    
    # 4. Use Isolation Forest for ML-based anomaly detection
    try:
        features_for_ml = df[['amount']].copy()
        
        # Add more features if available
        if 'date' in df.columns and 'hour' in df.columns:
            features_for_ml['hour'] = df['hour']
            features_for_ml['day_of_week'] = df['date'].dt.dayofweek
        
        # Normalize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_for_ml)
        
        # Apply Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        predictions = iso_forest.fit_predict(features_scaled)
        
        # Add ML anomalies
        anomaly_indices = np.where(predictions == -1)[0]
        for idx in anomaly_indices:
            original_idx = df.iloc[idx].name
            results["anomalies"].append({
                "type": "ML-Detected Anomaly",
                "index": int(original_idx),
                "amount": float(df.iloc[idx]['amount']),
                "reason": "Detected as anomalous by machine learning algorithm",
                "severity": "medium"
            })
    except Exception as e:
        results["alerts"].append(f"ML analysis error: {str(e)}")
    
    # 5. Detect structuring (multiple transactions just below reporting threshold)
    # Common threshold is $10,000
    structuring_threshold = 10000
    near_threshold = df[(df['amount'] > structuring_threshold * 0.8) & (df['amount'] < structuring_threshold)]
    
    if len(near_threshold) > 3:
        results["alerts"].append(f"{len(near_threshold)} transactions near ${structuring_threshold} threshold (possible structuring)")
        results["anomalies"].append({
            "type": "Potential Structuring",
            "count": len(near_threshold),
            "reason": f"Multiple transactions between ${structuring_threshold * 0.8:.0f} and ${structuring_threshold}",
            "severity": "high"
        })
    
    # Calculate overall risk score (0-100)
    risk_factors = 0
    if len(results["anomalies"]) > 5:
        risk_factors += 30
    elif len(results["anomalies"]) > 2:
        risk_factors += 15
    
    if len(results["alerts"]) > 3:
        risk_factors += 25
    elif len(results["alerts"]) > 1:
        risk_factors += 10
    
    high_severity_count = sum(1 for a in results["anomalies"] if a.get("severity") == "high")
    risk_factors += high_severity_count * 15
    
    results["risk_score"] = min(100, risk_factors)
    
    return results


def get_risk_level(risk_score):
    """Convert numeric risk score to risk level"""
    if risk_score >= 70:
        return "HIGH RISK", "🔴"
    elif risk_score >= 40:
        return "MEDIUM RISK", "🟡"
    elif risk_score >= 20:
        return "LOW RISK", "🟢"
    else:
        return "MINIMAL RISK", "✅"


def validate_transaction_csv(df):
    """
    Validate that CSV has required columns
    Returns: dict with is_valid, message, missing_columns
    """
    required_columns = ['amount']
    recommended_columns = ['date', 'transaction_type', 'description']
    
    missing_required = [col for col in required_columns if col not in df.columns]
    missing_recommended = [col for col in recommended_columns if col not in df.columns]
    
    if missing_required:
        return {
            "is_valid": False,
            "message": f"Missing required columns: {', '.join(missing_required)}",
            "missing_required": missing_required,
            "missing_recommended": missing_recommended
        }
    
    return {
        "is_valid": True,
        "message": "CSV structure is valid",
        "missing_required": [],
        "missing_recommended": missing_recommended
    }
