# backend/app/lib/enrichment.py

import socket
import os
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # absolute dir of enrichment.py
ASN_DB = os.path.join(BASE_DIR, "geolite", "GeoLite2-ASN.mmdb")
COUNTRY_DB = os.path.join(BASE_DIR, "geolite", "GeoLite2-Country.mmdb")

try:
    import geoip2.database
    print(f"[Enrichment] Trying DBs:\n ASN={ASN_DB}\n Country={COUNTRY_DB}")
    asn_reader = geoip2.database.Reader(ASN_DB)
    country_reader = geoip2.database.Reader(COUNTRY_DB)
    GEOIP_AVAILABLE = True
    print("[Enrichment] GeoIP databases loaded successfully")
except Exception as e:
    GEOIP_AVAILABLE = False
    asn_reader = None
    country_reader = None
    print(f"[Enrichment] Failed to load GeoIP: {e}")
    traceback.print_exc()


def enrich_ip(ip_address: str):
    if not GEOIP_AVAILABLE:
        return {}
    try:
        asn = asn_reader.asn(ip_address)
        country = country_reader.country(ip_address)
        return {
            "asn": f"AS{asn.autonomous_system_number} {asn.autonomous_system_organization}",
            "country": country.country.iso_code,
        }
    except Exception:
        return {}

def enrich_domain(domain: str):
    try:
        ip = socket.gethostbyname(domain)
        return enrich_ip(ip)
    except Exception:
        return {}
