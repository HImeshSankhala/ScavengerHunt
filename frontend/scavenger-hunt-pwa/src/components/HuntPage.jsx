import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { QrCode, MapPin, LogOut, Trophy, Camera } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import QRScanner from './QRScanner'

export function HuntPage() {
  const { user, logout, apiCall } = useAuth()
  const [currentStep, setCurrentStep] = useState(null)
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [showScanner, setShowScanner] = useState(false)
  const [huntCompleted, setHuntCompleted] = useState(false)

  useEffect(() => {
    loadCurrentStep()
  }, [])

  const loadCurrentStep = async () => {
    try {
      setLoading(true)
      const data = await apiCall('/hunt/current-step')
      
      if (data.completed) {
        setHuntCompleted(true)
      } else {
        setCurrentStep(data.step)
        setProgress(data.progress)
      }
    } catch (error) {
      setError('Failed to load current step')
    } finally {
      setLoading(false)
    }
  }

  const handleRevealLocation = async () => {
    try {
      const data = await apiCall('/hunt/reveal-location', { method: 'POST' })
      setSuccess(data.message)
      // Reload current step to update revealed status
      loadCurrentStep()
    } catch (error) {
      setError('Failed to reveal location')
    }
  }

  const handleQRScan = async (qrValue) => {
    console.log('🎯 HuntPage: Received QR scan result:', qrValue)
    console.log('🔄 HuntPage: Starting QR processing...')
    
    try {
      setError('')
      setSuccess('')
      
      console.log('📡 HuntPage: Sending QR to backend API...')
      const data = await apiCall('/hunt/scan-qr', {
        method: 'POST',
        body: JSON.stringify({ qr_value: qrValue })
      })

      console.log('📥 HuntPage: Backend response:', data)

      if (data.success) {
        console.log('✅ HuntPage: QR scan successful!')
        console.log('🎉 HuntPage: Success message:', data.message)
        
        setSuccess(data.message)
        setShowScanner(false)
        
        if (data.completed_hunt) {
          console.log('🏆 HuntPage: Hunt completed!')
          setHuntCompleted(true)
        } else if (data.next_step) {
          console.log('➡️ HuntPage: Moving to next step:', data.next_step)
          setCurrentStep(data.next_step)
          // Reload progress
          console.log('🔄 HuntPage: Reloading progress...')
          loadCurrentStep()
        }
        
        console.log('🚀 HuntPage: QR scan processing completed successfully!')
      } else {
        console.log('❌ HuntPage: QR scan failed:', data.message)
        setError(data.message)
      }
    } catch (error) {
      console.error('💥 HuntPage: QR scan error:', error)
      setError('Failed to process QR scan')
    }
  }

  const progressPercentage = progress ? (progress.completed_steps.length / progress.total) * 100 : 0

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-orange-600">Loading your adventure...</p>
        </div>
      </div>
    )
  }

  if (huntCompleted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 flex items-center justify-center p-4">
        <Card className="w-full max-w-md text-center shadow-lg">
          <CardHeader>
            <div className="mx-auto mb-4">
              <Trophy className="h-16 w-16 text-yellow-500" />
            </div>
            <CardTitle className="text-2xl text-green-600">Congratulations!</CardTitle>
            <CardDescription>
              You've completed the Milwaukee Scavenger Hunt!
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-green-700">
              🎉 You've discovered all 13 locations and solved every clue. 
              Great job exploring Milwaukee!
            </p>
            <Button onClick={logout} variant="outline" className="w-full">
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-xl font-bold text-orange-600">Scavenger Hunt</h1>
          <Button onClick={logout} variant="ghost" size="sm">
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="max-w-md mx-auto p-4 space-y-6">
        {/* Progress */}
        {progress && (
          <Card>
            <CardContent className="pt-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Progress</span>
                  <span>{progress.completed_steps.length} / {progress.total}</span>
                </div>
                <Progress value={progressPercentage} className="h-2" />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Step {progress.current}</span>
                  <span>{Math.round(progressPercentage)}% Complete</span>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Current Clue Card */}
        {currentStep && (
          <Card className="shadow-lg border-2 border-orange-200 bg-gradient-to-br from-orange-50 to-yellow-50">
            <CardHeader className="text-center">
              <div className="flex items-center justify-center space-x-2 mb-2">
                <Badge variant="secondary">Step {progress?.current}</Badge>
                {progress?.revealed_locations.includes(progress?.current) && (
                  <Badge variant="outline" className="text-green-600 border-green-600">
                    <MapPin className="h-3 w-3 mr-1" />
                    Revealed
                  </Badge>
                )}
              </div>
              <CardTitle className="text-lg text-orange-700">Find Your Next Location</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center p-4 bg-white rounded-lg border border-orange-200">
                <p className="text-gray-700 text-lg leading-relaxed">
                  "{currentStep.clue}"
                </p>
              </div>

              {/* Revealed Location */}
              {progress?.revealed_locations.includes(progress?.current) && (
                <Alert className="border-green-200 bg-green-50">
                  <MapPin className="h-4 w-4" />
                  <AlertDescription className="text-green-700 font-medium">
                    Location: {currentStep.name}
                  </AlertDescription>
                </Alert>
              )}

              {/* Action Buttons */}
              <div className="space-y-3">
                <Button 
                  onClick={() => setShowScanner(true)}
                  className="w-full bg-orange-500 hover:bg-orange-600 text-white"
                  size="lg"
                >
                  <Camera className="h-5 w-5 mr-2" />
                  Scan QR Code
                </Button>

                {!progress?.revealed_locations.includes(progress?.current) && (
                  <Button 
                    onClick={handleRevealLocation}
                    variant="outline"
                    className="w-full border-orange-300 text-orange-600 hover:bg-orange-50"
                  >
                    <MapPin className="h-4 w-4 mr-2" />
                    Reveal Location
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Messages */}
        {error && (
          <Alert className="border-red-200 bg-red-50">
            <AlertDescription className="text-red-700">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert className="border-green-200 bg-green-50">
            <AlertDescription className="text-green-700">
              {success}
            </AlertDescription>
          </Alert>
        )}

        {/* User Info */}
        <Card className="bg-white/50">
          <CardContent className="pt-6">
            <div className="text-center text-sm text-gray-600">
              <p>Signed in as: {user?.email || user?.phone}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* QR Scanner Modal */}
      {showScanner && (
        <QRScanner 
          onScan={handleQRScan}
          onClose={() => setShowScanner(false)}
        />
      )}
    </div>
  )
}

