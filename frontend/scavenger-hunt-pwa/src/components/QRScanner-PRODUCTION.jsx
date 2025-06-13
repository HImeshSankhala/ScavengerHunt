import { useState, useEffect, useRef } from 'react'
import { BrowserMultiFormatReader } from '@zxing/library'

const QRScanner = ({ onScan, onClose }) => {
  const [isScanning, setIsScanning] = useState(false)
  const [error, setError] = useState('')
  const [manualInput, setManualInput] = useState('')
  const [showManualInput, setShowManualInput] = useState(false)
  const videoRef = useRef(null)
  const codeReaderRef = useRef(null)

  useEffect(() => {
    return () => {
      stopScanning()
    }
  }, [])

  const startScanning = async () => {
    console.log('🎥 Starting QR scanner...')
    try {
      setError('')
      setIsScanning(true)
      
      // Initialize the code reader
      codeReaderRef.current = new BrowserMultiFormatReader()
      
      // Get video devices
      const videoDevices = await codeReaderRef.current.listVideoInputDevices()
      console.log('📱 Available cameras:', videoDevices.length)
      
      if (videoDevices.length === 0) {
        throw new Error('No camera devices found')
      }

      // Use back camera if available (for mobile)
      const selectedDevice = videoDevices.find(device => 
        device.label.toLowerCase().includes('back') || 
        device.label.toLowerCase().includes('rear')
      ) || videoDevices[0]
      
      console.log('📷 Using camera:', selectedDevice.label)

      // Start decoding
      const result = await codeReaderRef.current.decodeOnceFromVideoDevice(
        selectedDevice.deviceId,
        videoRef.current
      )
      
      if (result) {
        const scannedText = result.getText()
        console.log('✅ QR CODE SUCCESSFULLY SCANNED:', scannedText)
        console.log('🎯 Processing scanned QR code...')
        
        // Stop scanning immediately
        stopScanning()
        
        // Call the onScan callback with the scanned text
        console.log('📤 Sending QR code to parent component:', scannedText)
        onScan(scannedText)
        
        console.log('🚀 QR scan success flow completed!')
      }
      
    } catch (err) {
      console.error('❌ QR Scanner Error:', err)
      setError(`Camera error: ${err.message}`)
      setIsScanning(false)
    }
  }

  const stopScanning = () => {
    console.log('🛑 Stopping QR scanner...')
    if (codeReaderRef.current) {
      codeReaderRef.current.reset()
      codeReaderRef.current = null
    }
    setIsScanning(false)
  }

  const handleManualSubmit = () => {
    if (manualInput.trim()) {
      console.log('✏️ MANUAL QR CODE ENTERED:', manualInput.trim())
      console.log('🎯 Processing manual QR code...')
      onScan(manualInput.trim())
      console.log('🚀 Manual QR scan success flow completed!')
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Scan QR Code</h3>
          <button 
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl"
          >
            ×
          </button>
        </div>

        {/* Camera Section */}
        {isScanning ? (
          <div className="mb-4">
            <div className="relative bg-black rounded-lg overflow-hidden">
              <video 
                ref={videoRef}
                className="w-full h-64 object-cover"
                autoPlay
                playsInline
                muted
              />
              {/* Scanning overlay with corners */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="relative w-48 h-48 border-2 border-orange-500 rounded-lg">
                  {/* Corner indicators */}
                  <div className="absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4 border-orange-500"></div>
                  <div className="absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4 border-orange-500"></div>
                  <div className="absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4 border-orange-500"></div>
                  <div className="absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4 border-orange-500"></div>
                </div>
              </div>
              <div className="absolute bottom-4 left-0 right-0 text-center">
                <p className="text-white bg-black bg-opacity-50 px-3 py-1 rounded">
                  Point camera at QR code
                </p>
              </div>
            </div>
            <button 
              onClick={stopScanning}
              className="w-full mt-3 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
            >
              Stop Scanning
            </button>
          </div>
        ) : (
          <button 
            onClick={startScanning}
            className="w-full mb-4 px-4 py-3 bg-orange-600 text-white rounded hover:bg-orange-700 flex items-center justify-center gap-2"
          >
            📷 Start Camera Scan
          </button>
        )}

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Manual Input Section */}
        <button 
          onClick={() => setShowManualInput(!showManualInput)}
          className="w-full mb-4 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
        >
          ✏️ Manual Input
        </button>

        {showManualInput && (
          <div className="mb-4 space-y-2">
            <input
              type="text"
              value={manualInput}
              onChange={(e) => setManualInput(e.target.value)}
              placeholder="Enter QR code text"
              className="w-full px-3 py-2 border border-gray-300 rounded"
              onKeyPress={(e) => e.key === 'Enter' && handleManualSubmit()}
            />
            <button 
              onClick={handleManualSubmit}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Submit
            </button>
          </div>
        )}

        {/* Valid QR codes info */}
        <div className="mt-3 text-xs text-gray-400 text-center">
          <p>Valid QR codes:</p>
          <p>BLACKCAT_ALLEY_001 • ART_MUSEUM_002 • DISCOVERY_WORLD_003</p>
        </div>
      </div>
    </div>
  )
}

export default QRScanner

