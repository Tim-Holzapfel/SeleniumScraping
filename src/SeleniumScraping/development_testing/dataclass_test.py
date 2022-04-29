
from dataclasses import dataclass, asdict

@dataclass
class Settings:
    app_shield_optoutstudies_enabled: bool = True
    app_update_BITS_enabled: bool = False
    app_update_auto_migrated: bool = False
    app_update_background_experimental: bool = False
    app_update_background_scheduling_enabled: bool = False
    app_update_service_enabled: bool = False
    beacon_enabled: bool = False
    browser_cache_disk_enable: bool = True
    browser_cache_disk_cache_ssl: bool = True
    browser_cache_memory_enable: bool = True
    browser_cache_offline_enable: bool = False
    browser_display_show_image_placeholders: bool = False
    browser_formfill_enable: bool = False
    browser_privatebrowsing_autostart: bool = True
    browser_safebrowsing_downloads_enabled: bool = False
    browser_safebrowsing_downloads_remote_url: str = ""
    browser_safebrowsing_enabled: bool = False
    browser_safebrowsing_malware_enabled: bool = False
    browser_safebrowsing_phishing_enabled: bool = False
    browser_safebrowsing_provider_google_advisoryURL: str = ""
    browser_safebrowsing_provider_google_gethashURL: str = ""
    browser_safebrowsing_provider_google_lists: str = ""
    browser_safebrowsing_provider_google_pver: str = ""
    browser_safebrowsing_provider_google_reportMalwareMistakeURL: str = ""
    browser_safebrowsing_provider_google_reportPhishMistakeURL: str = ""
    browser_safebrowsing_provider_google_reportURL : str = ""
    browser_safebrowsing_provider_google_updateURL: str = ""
    browser_safebrowsing_provider_google4_advisoryName: str = ""
    browser_safebrowsing_provider_google4_advisoryURL: str = ""
    browser_safebrowsing_provider_google4_dataSharing_enabled: str = ""
    browser_safebrowsing_provider_google4_dataSharingURL: str = ""
    browser_safebrowsing_provider_google4_gethashURL: str = ""
    browser_safebrowsing_provider_google4_lists: str = ""
    browser_safebrowsing_provider_google4_reportMalwareMistakeURL: str = ""
    browser_safebrowsing_provider_google4_reportPhishMistakeURL: str = ""
    browser_safebrowsing_provider_google4_reportURL: str = ""
    browser_safebrowsing_provider_google4_updateURL: str = ""
    browser_search_geoip_url: str = ""
    browser_search_suggest_enabled: bool = False
    browser_selfsupport_url: bool = False
    browser_send_pings: bool = False
    browser_tabs_disableBackgroundZombification: bool = True
    browser_tabs_loadInBackground: bool = False
    browser_zoom_updateBackgroundTabs: bool = False
    browserName: str = "firefox"
    doh__rollout_home__region: str = "US"
    dom_battery_enabled: bool = False
    dom_event_clipboardevents_enabled: bool = False
    extensions_autoDisableScopes: int = 0
    extensions_enabledScopes: int = 15
    extensions_systemAddon_update_enabled: bool = False
    extensions_webextensions_background__delayed__startup: bool = False
    general_useragent_locale: str = "en-US"
    geo_enabled: bool = False
    geo_wifi_uri: str = ""
    javascript: bool = True
    media_peerconnection_enabled: bool = False
    network_IDN_show_punycode: bool = True
    network_cookie_cookieBehavior: int = 1
    network_dns_disablePrefetch: bool = True
    network_dns_disablePrefetchFromHTTPS: bool = True
    network_http_speculative__parallel__limit: int = 0
    network_http_use__cache: bool = False
    network_predictor_enable__prefetch: bool = False
    network_prefetch__next: bool = False
    network_proxy_socks: str = "127_0_0_1"
    network_proxy_socks_port: int = 9150
    network_proxy_socks_remote_dns: bool = True
    network_proxy_socks_version: int = 5
    network_proxy_type: int = 1
    network_websocket_enabled: bool = False
    permissions_default_geo: int = 2
    permissions_default_image: int = 2
    places_history_enabled: bool = False
    plugin_scan_plid_all: bool = False
    plugin_state_flash: int = 0
    port: int = 4444
    privacy_antitracking_testing: bool = True
    privacy_clearOnShutdown_history: bool = True
    privacy_clearOnShutdown_offlineApps: bool = True
    privacy_clearOnShutdown_openWindows: bool = True
    privacy_clearOnShutdown_siteSettings: bool = True
    privacy_cpd_cache: bool = False
    privacy_cpd_cookies: bool = False
    privacy_cpd_history: bool = False
    privacy_donottrackheader_enabled: bool = True
    privacy_firstparty_isolate: bool = True
    privacy_partition_network_state_connection_with_proxy: bool = True
    privacy_purge_trackers_enabled: bool = True
    privacy_resistFingerprinting: bool = True
    privacy_sanitize_sanitizeOnShutdown: bool = True
    privacy_spoof_english: int = 1
    privacy_trackingprotection_enabled: bool = True
    privacy_trackingprotection_lower_network_priority: bool = True
    remoteServerAddr: str = "localhost"
    services_sync_engine_history: bool = False
    services_sync_prefs_sync_browser_startup_homepage: bool = False
    toolkit_legacyUserProfileCustomizations_stylesheets: bool = True
    xpinstall_signatures_required: bool = False



type(Settings)




import regex as re



def replace_keys(input_data):
    input_dict = asdict(input_data)
    output_dict = {re.sub("__", "-", k): v for k, v in input_dict.items()}
    output_dict = {re.sub("_", ".", k): v for k, v in output_dict.items()}
    return output_dict



t1 = replace_keys(Settings())









t1 = asdict(browser_settings)




t3 = "app_shield__optoutstudies_enabled"

dict_rename = re.sub("_", ".", t3)




re.DEFAULT_VERSION = re.VERSION1




