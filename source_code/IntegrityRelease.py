import os

variant = "TegraP1Integrity.Rel.B0hw.C5.MRA2"
#
#  Define spaces and domains
#
releaseInfo.SourceSpace = 'SourceSpace'
releaseInfo.ProductSpace = 'ProductSpace'
releaseInfo.AdditionalDir = ''
releaseInfo.AddDomain('InternalIF')
releaseInfo.AddDomain('SharedLIBs')
releaseInfo.AddDomain('SharedConfig')

releaseInfo. ExcludeBun ('InternalIF.DiagAPI')
releaseInfo. ExcludeBun ('SharedLIBs.IPMessage')
releaseInfo. ExcludeBun ('SharedConfig.HILConfig')

# Keep the other releases in the directory
#
#releaseInfo.AddDstExcludePatterns('TegraP1Integrity.Dbg')
#releaseInfo.AddDstExcludePatterns('TegraP1Lin.Dbg')
#releaseInfo.AddDstExcludePatterns('X86Lin.Dbg')


#
#  Lots of variants to release
#
releaseInfo.AddVariant(variant)
