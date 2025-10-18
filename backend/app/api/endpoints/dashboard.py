from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.olt import OLT as OLTModel
from app.models.onu import ONU as ONUModel
from app.models.odp import ODP as ODPModel

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    # Count OLTs
    total_olts = db.query(OLTModel).count()
    online_olts = db.query(OLTModel).filter(OLTModel.status == "online").count()
    offline_olts = db.query(OLTModel).filter(OLTModel.status == "offline").count()
    
    # Count ONUs
    total_onus = db.query(ONUModel).count()
    online_onus = db.query(ONUModel).filter(ONUModel.status == "online").count()
    offline_onus = db.query(ONUModel).filter(ONUModel.status == "offline").count()
    
    # Count ODPs
    total_odps = db.query(ODPModel).count()
    active_odps = db.query(ODPModel).filter(ODPModel.status == "active").count()
    
    # Calculate port utilization
    total_ports = db.query(func.sum(ODPModel.total_ports)).scalar() or 0
    used_ports = db.query(func.sum(ODPModel.used_ports)).scalar() or 0
    port_utilization = (used_ports / total_ports * 100) if total_ports > 0 else 0
    
    return {
        "olts": {
            "total": total_olts,
            "online": online_olts,
            "offline": offline_olts
        },
        "onus": {
            "total": total_onus,
            "online": online_onus,
            "offline": offline_onus
        },
        "odps": {
            "total": total_odps,
            "active": active_odps
        },
        "port_utilization": round(port_utilization, 2)
    }


@router.get("/recent-onus")
def get_recent_onus(limit: int = 10, db: Session = Depends(get_db)):
    """Get recently added ONUs"""
    onus = db.query(ONUModel).order_by(ONUModel.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": onu.id,
            "sn": onu.sn,
            "customer_name": onu.customer_name,
            "status": onu.status,
            "created_at": onu.created_at
        }
        for onu in onus
    ]


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    """Get system alerts"""
    alerts = []
    
    # Check offline OLTs
    offline_olts = db.query(OLTModel).filter(OLTModel.status == "offline").all()
    for olt in offline_olts:
        alerts.append({
            "type": "error",
            "title": "OLT Offline",
            "message": f"OLT {olt.name} is offline",
            "timestamp": olt.last_seen
        })
    
    # Check offline ONUs
    offline_onus_count = db.query(ONUModel).filter(ONUModel.status == "offline").count()
    if offline_onus_count > 0:
        alerts.append({
            "type": "warning",
            "title": "Offline ONUs",
            "message": f"{offline_onus_count} ONUs are offline",
            "timestamp": None
        })
    
    # Check low signal ONUs
    low_signal_onus = db.query(ONUModel).filter(
        ONUModel.rx_power < -27
    ).count()
    if low_signal_onus > 0:
        alerts.append({
            "type": "warning",
            "title": "Low Signal ONUs",
            "message": f"{low_signal_onus} ONUs have low signal strength",
            "timestamp": None
        })
    
    return alerts
