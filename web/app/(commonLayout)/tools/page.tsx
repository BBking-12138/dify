'use client'
import type { FC } from 'react'
import { useTranslation } from 'react-i18next'
import React, { useEffect } from 'react'
import ToolProviderList from '@/app/components/tools/provider-list'

const Layout: FC = () => {
  const { t } = useTranslation()

  useEffect(() => {
    document.title = `${t('tools.title')} - haizhi`
  }, [])

  return <ToolProviderList />
}
export default React.memo(Layout)
