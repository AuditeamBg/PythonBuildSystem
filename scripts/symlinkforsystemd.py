import yaml
import sys
import os
from subprocess import call
from glob import glob


if __name__ == '__main__':
    os.environ["WORKSPACE_PATH"]            = os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"]
    os.environ["TARGETFS"]                  = os.environ["WORKSPACE_PATH"] + "/cards/Mra2-SOC-C5v" + os.environ["ITERATION_NUMBER_C5"] + "." + os.environ["BUILD_NUMBER"] + "/drive-t186ref-linux/out/targetfs"
    os.environ["SYSTEMD_NETWORKING"]        = os.environ["TARGETFS"]  + "/opt/visteon/etc/nm/system/"
    os.environ["SYSTEMD"]                   = os.environ["TARGETFS"]  + "/etc/systemd/system/"
    os.environ["LIB"]                       = os.environ["TARGETFS"]  + "/lib/systemd/system/"
    os.environ["PATH_TO_BIN"]               = os.environ["TARGETFS"]  + "/usr/bin/"
    os.environ["MULTI-USER-TARGET-WANTS"]   = os.environ["TARGETFS"]  + "/etc/systemd/system/multi-user.target.wants/"

    lib                                     = os.environ["LIB"]
    usrBin                                  = os.environ["PATH_TO_BIN"]
    systemd                                 = os.environ["SYSTEMD"]
    systemd_networking                      = os.environ["SYSTEMD_NETWORKING"]
    multi_user_target_wants                 = os.environ["MULTI-USER-TARGET-WANTS"]

    Tuner_service                           = os.environ["SYSTEMD"] + "Tuner.service"
    Traceserver_service                     = os.environ["SYSTEMD"] + "TraceServer.service" 
    TunerIF1_service                        = os.environ["SYSTEMD"] + "TunerIF1.service"
    AudioIF1_service                        = os.environ["SYSTEMD"] + "AudioIF1.service"
    app_audio_service                       = os.environ["SYSTEMD"] + "app_audio.service"
    app_carocore_service                    = os.environ["SYSTEMD"] + "app_carocore.service"
    MainIF1_service                         = os.environ["SYSTEMD"] + "MainIF1.service"
    GDMService_service                      = os.environ["SYSTEMD"] + "GDMService.service"
    frontend_service                        = os.environ["SYSTEMD"] + "frontend.service"
    remoteui_service                        = os.environ["SYSTEMD"] + "app_remoteui.service"
    remoteui_if1service                     = os.environ["SYSTEMD"] + "RemoteUI_IF1.service"
    mediabase_service                       = os.environ["SYSTEMD"] + "app_media.service"
    app_playerIF1_service                   = os.environ["SYSTEMD"] + "app_playerIF1.service"
    configure_core_service                  = os.environ["SYSTEMD"] + "configure_core.service"
    app_measurements_service                = os.environ["SYSTEMD"] + "app_measurements.service"
    IVIOnOff_service                        = os.environ["SYSTEMD"] + "IVIOnOff.service"
    app_networkmanager_service              = os.environ["SYSTEMD"] + "app_networkmanager.service"
    app_comamra2hostedbt_service            = os.environ["SYSTEMD"] + "app_comamra2hostedbt.service"
    app_comamra2hostedbtTest_service        = os.environ["SYSTEMD"] + "app_comamra2hostedbttest.service"
    IVI_Persistency_service                 = os.environ["SYSTEMD"] + "IVIPersistency.service"
    IVI_Diagnostic_service                  = os.environ["SYSTEMD"] + "IVIDiagnostic.service"
    app_firewall_service                    = os.environ["SYSTEMD"] + "app_firewall.service"

    dnsmasq_service                         = os.environ["SYSTEMD_NETWORKING"] + "dnsmasq@.service"    
    hostapd_service                         = os.environ["SYSTEMD_NETWORKING"] + "hostapd.service"
    udhcpd_service                          = os.environ["SYSTEMD_NETWORKING"] + "udhcpd.service"
    wpa_supplicant_service                  = os.environ["SYSTEMD_NETWORKING"] + "wpa_supplicant.service"


    link_to_delete  = multi_user_target_wants + "dnsmasq.service" 
    link_to_delete2 = systemd + "dnsmasq@.service"
    link_to_delete3 = systemd + "hostapd.service"
    link_to_delete4 = lib + "dnsmasq.service"
    link_to_delete5 = lib + "hostapd.service"
    bin_to_remove   = usrBin + "start_connmand.sh"

    services = []
    services.append(Tuner_service)
    services.append(Traceserver_service)
    services.append(TunerIF1_service)
    services.append(AudioIF1_service)
    services.append(app_audio_service)
    services.append(app_carocore_service)
    services.append(MainIF1_service)
    services.append(GDMService_service)
    services.append(frontend_service)
    services.append(app_comamra2hostedbt_service)
    services.append(app_comamra2hostedbtTest_service)
    services.append(remoteui_service)
    services.append(remoteui_if1service)
    services.append(mediabase_service)
    services.append(app_playerIF1_service)
    services.append(configure_core_service)
    services.append(app_measurements_service)
    services.append(IVIOnOff_service)
    services.append(app_networkmanager_service)
    services.append(IVI_Persistency_service)
    services.append(IVI_Diagnostic_service)
    #services.append(app_firewall_service)

    service_networking = []
    service_networking.append(udhcpd_service)
    service_networking.append(wpa_supplicant_service)

    service_networking_2 = []
    service_networking_2.append(dnsmasq_service)
    service_networking_2.append(hostapd_service)

    service_to_unlink = []
    service_to_unlink.append(bin_to_remove)
    service_to_unlink.append(link_to_delete)
    service_to_unlink.append(link_to_delete2)
    service_to_unlink.append(link_to_delete3)
    service_to_unlink.append(link_to_delete4)
    service_to_unlink.append(link_to_delete5)


    for target in service_to_unlink:
        print "Current Target:",target
        if "dnsmasq.service" in target:
            os.system("unlink  %s " % (target))
        else:
            os.system("rm -f %s " % (target))


    for target in services:
        print "Current Target:",target
        os.system("ln -sr %s %s" % (target,multi_user_target_wants))
        #os.symlink(target,multi_user_target_wants)
        

    for target in service_networking:
        print "Current Target:",target
        os.system("ln -sr %s %s" % (target,multi_user_target_wants))
    
    for target in service_networking_2:
        print "Current Target:",target
        os.system("ln -sr %s %s" % (target,systemd))

    print "[symlinkforsystemd.py] finished with Success"
 

