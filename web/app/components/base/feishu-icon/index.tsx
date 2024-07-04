import cn from 'classnames'
import s from './index.module.css'
import type { DataSourceFeishuPage } from '@/models/common'

type IconTypes = 'workspace' | 'page'
type FeishuIconProps = {
  type?: IconTypes
  name?: string | null
  className?: string
  src?: string | null | DataSourceFeishuPage['page_icon']
}
const FeishuIcon = ({
  type = 'workspace',
  src,
  name,
  className,
}: FeishuIconProps) => {
  if (type === 'workspace') {
    if (typeof src === 'string') {
      if (src.startsWith('https://') || src.startsWith('http://')) {
        return (
          <img
            alt='workspace icon'
            src={src}
            className={cn('block object-cover w-5 h-5', className)}
          />
        )
      }
      return (
        <div className={cn('flex items-center justify-center w-5 h-5', className)}>{src}</div>
      )
    }
    return (
      <div className={cn('flex items-center justify-center w-5 h-5 bg-gray-200 text-xs font-medium text-gray-500 rounded', className)}>{name?.[0].toLocaleUpperCase()}</div>
    )
  }

  if (typeof src === 'object' && src !== null) {
    if (src?.type === 'url') {
      return (
        <img
          alt='page icon'
          src={src.url || ''}
          className={cn('block object-cover w-5 h-5', className)}
        />
      )
    }
    return (
      <div className={cn('flex items-center justify-center w-5 h-5', className)}>{src?.emoji}</div>
    )
  }

  return (
    <div className={cn(s['default-page-icon'], className)} />
  )
}

export default FeishuIcon
