import os

variant = "TegraP1Lin.Rel.B0hw.C5.MRA2"
#
#  Define spaces and domains
#
releaseInfo.SourceSpace = 'SourceSpace'
releaseInfo.ProductSpace = 'ProductSpace'
releaseInfo.AdditionalDir = ''
releaseInfo.AddDomain('IF1')
releaseInfo.AddDomain('InternalIF')
releaseInfo.AddDomain('DiagnosticsIVI')
releaseInfo.AddDomain('Persistency')
releaseInfo.AddDomain('IVI')
releaseInfo.AddDomain('TunerIF1')
releaseInfo.AddDomain('SharedConfig')
releaseInfo.AddDomain('Audio')

#
# Keep the other releases in the directory
#
#releaseInfo.AddDstExcludePatterns('TegraP1Integrity.Dbg')
#releaseInfo.AddDstExcludePatterns('TegraP1Lin.Dbg')
#releaseInfo.AddDstExcludePatterns('X86Lin.Dbg')


#
#  Lots of variants to release
#
releaseInfo.AddVariant(variant)
