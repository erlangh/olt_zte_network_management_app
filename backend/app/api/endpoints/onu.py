from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.olt import OLT, Slot, Port
from app.models.onu import ONU
from app.services.snmp_client import SNMPClient

router = APIRouter(prefix="/onu", tags=["ONU"])


@router.get("/olt/{olt_id}/discover")
def discover_onus(olt_id: int, db: Session = Depends(get_db)):
    olt = db.query(OLT).filter(OLT.id == olt_id).first()
    if not olt:
        raise HTTPException(status_code=404, detail="OLT not found")

    client = SNMPClient(host=olt.host, community=olt.community)

    # Walk ONUs via SNMP
    discovered = client.get_onu_list()
    if not discovered:
        return {"found": 0, "created": 0, "updated": 0}

    created = 0
    updated = 0

    # Ensure Slot and Port exist; then upsert ONU using SN
    for item in discovered:
        slot_no = item["slot"]
        port_no = item["port"]
        onu_id = item["onu_id"]
        status = item.get("status")
        suffix_raw = item.get("oid_suffix")

        # Fetch details using raw suffix (ZTE encodes port index)
        details = client.get_onu_details_suffix(suffix_raw)
        sn = details.get("sn")
        if not sn:
            # Skip if SN missing; cannot upsert reliably
            continue

        # Create or get Slot
        slot = (
            db.query(Slot)
            .filter(Slot.olt_id == olt.id, Slot.slot_number == slot_no)
            .first()
        )
        if not slot:
            slot = Slot(olt_id=olt.id, slot_number=slot_no)
            db.add(slot)
            db.flush()

        # Create or get Port (decoded port number)
        port = (
            db.query(Port)
            .filter(Port.olt_id == olt.id, Port.slot_id == slot.id, Port.port_number == port_no)
            .first()
        )
        if not port:
            port = Port(olt_id=olt.id, slot_id=slot.id, port_number=port_no)
            db.add(port)
            db.flush()

        # Upsert ONU by serial number
        onu = db.query(ONU).filter(ONU.sn == sn).first()
        if onu:
            # Update existing ONU
            onu.olt_id = olt.id
            onu.port_id = port.id
            onu.onu_id = onu_id
            onu.status = status
            onu.rx_power = details.get("rx_power")
            onu.tx_power = details.get("tx_power")
            onu.distance = details.get("distance")
            updated += 1
        else:
            # Create new ONU
            onu = ONU(
                olt_id=olt.id,
                port_id=port.id,
                onu_id=onu_id,
                sn=sn,
                status=status,
                rx_power=details.get("rx_power"),
                tx_power=details.get("tx_power"),
                distance=details.get("distance"),
            )
            db.add(onu)
            created += 1

    db.commit()

    return {"found": len(discovered), "created": created, "updated": updated}
