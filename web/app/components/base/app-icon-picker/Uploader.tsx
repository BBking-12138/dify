'use client'

import { FC, ChangeEvent, useState, useEffect, createRef } from 'react'
import Cropper, { Area } from 'react-easy-crop'
import classNames from "classnames"

import { useDraggableUploader } from "./hooks"
import { ImagePlus } from "../icons/src/vender/line/images"
import { ALLOW_FILE_EXTENSIONS, ImageFile } from "@/types/app"

interface UploaderProps {
    className?: string
    onImageCropped?: (tempUrl: string, croppedAreaPixels: Area, fileName: string) => void
}

const Uploader: FC<UploaderProps> = ({
    className,
    onImageCropped,
}) => {
    const [inputImage, setInputImage] = useState<{ file: File, url: string }>()
    useEffect(() => {
        return () => {
            if (inputImage) URL.revokeObjectURL(inputImage.url);
        }
    }, [inputImage])

    const [crop, setCrop] = useState({ x: 0, y: 0 })
    const [zoom, setZoom] = useState(1)

    const onCropComplete = async (_: Area, croppedAreaPixels: Area) => {
        if (!inputImage) return
        onImageCropped?.(inputImage.url, croppedAreaPixels, inputImage.file.name)
    }

    const handleLocalFileInput = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) setInputImage({ file, url: URL.createObjectURL(file) })
    }

    const {
        isDragActive,
        handleDragEnter,
        handleDragOver,
        handleDragLeave,
        handleDrop
    } = useDraggableUploader((file: File) => setInputImage({ file, url: URL.createObjectURL(file) }))

    const inputRef = createRef<HTMLInputElement>()

    return (
        <div className="w-full px-3 py-1.5">
            <div
                className={classNames(className,
                    isDragActive && 'border-primary-600',
                    'relative aspect-square bg-gray-50 border-[1.5px] border-gray-200 border-dashed rounded-lg flex flex-col justify-center items-center text-gray-500')}
                onDragEnter={handleDragEnter}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                {
                    !inputImage
                        ? <>
                            <ImagePlus className="w-[30px] h-[30px] mb-3 pointer-events-none" />
                            <div className="text-sm font-medium mb-[2px]">
                                <span className="pointer-events-none">Drop your image here, or&nbsp;</span>
                                <button className="text-components-button-primary-bg" onClick={() => inputRef.current?.click()}>browse</button>
                                <input
                                    ref={inputRef} type="file" className="hidden"
                                    onClick={e => ((e.target as HTMLInputElement).value = '')}
                                    accept={ALLOW_FILE_EXTENSIONS.map(ext => `.${ext}`).join(',')}
                                    onChange={handleLocalFileInput}
                                />
                            </div>
                            <div className="text-xs pointer-events-none">Supports PNG, JPG, JPEG, WEBP and GIF</div>
                        </>
                        : <Cropper
                            image={inputImage.url}
                            crop={crop}
                            zoom={zoom}
                            aspect={1}
                            onCropChange={setCrop}
                            onCropComplete={onCropComplete}
                            onZoomChange={setZoom}
                        />
                }
            </div>
        </div>
    )
}

export default Uploader