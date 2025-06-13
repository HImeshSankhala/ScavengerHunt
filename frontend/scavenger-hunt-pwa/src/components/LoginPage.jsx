import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useAuth } from '../hooks/useAuth'

export function LoginPage() {
  const { login, adminLogin } = useAuth()
  const [userForm, setUserForm] = useState({ email: '', phone: '' })
  const [adminForm, setAdminForm] = useState({ username: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleUserLogin = async (e) => {
    e.preventDefault()
    if (!userForm.email && !userForm.phone) {
      setError('Please enter either email or phone number')
      return
    }

    setLoading(true)
    setError('')

    const result = await login(userForm.email, userForm.phone)
    
    if (!result.success) {
      setError(result.error)
    }
    
    setLoading(false)
  }

  const handleAdminLogin = async (e) => {
    e.preventDefault()
    if (!adminForm.username || !adminForm.password) {
      setError('Please enter username and password')
      return
    }

    setLoading(true)
    setError('')

    const result = await adminLogin(adminForm.username, adminForm.password)
    
    if (!result.success) {
      setError(result.error)
    }
    
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-orange-600 mb-2">🏃‍♂️ Scavenger Hunt</h1>
          <p className="text-orange-700">Explore Milwaukee with clues and QR codes!</p>
        </div>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-center text-orange-600">Welcome</CardTitle>
            <CardDescription className="text-center">
              Sign in to start your adventure
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="user" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="user">Player</TabsTrigger>
                <TabsTrigger value="admin">Admin</TabsTrigger>
              </TabsList>
              
              <TabsContent value="user" className="space-y-4">
                <form onSubmit={handleUserLogin} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Email</label>
                    <Input
                      type="email"
                      placeholder="your@email.com"
                      value={userForm.email}
                      onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                  
                  <div className="text-center text-sm text-gray-500">or</div>
                  
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Phone Number</label>
                    <Input
                      type="tel"
                      placeholder="(555) 123-4567"
                      value={userForm.phone}
                      onChange={(e) => setUserForm({ ...userForm, phone: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                  
                  <Button 
                    type="submit" 
                    className="w-full bg-orange-500 hover:bg-orange-600"
                    disabled={loading}
                  >
                    {loading ? 'Signing In...' : 'Start Hunt'}
                  </Button>
                </form>
              </TabsContent>
              
              <TabsContent value="admin" className="space-y-4">
                <form onSubmit={handleAdminLogin} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Username</label>
                    <Input
                      type="text"
                      placeholder="admin"
                      value={adminForm.username}
                      onChange={(e) => setAdminForm({ ...adminForm, username: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Password</label>
                    <Input
                      type="password"
                      placeholder="••••••••"
                      value={adminForm.password}
                      onChange={(e) => setAdminForm({ ...adminForm, password: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                  
                  <Button 
                    type="submit" 
                    className="w-full bg-gray-800 hover:bg-gray-900"
                    disabled={loading}
                  >
                    {loading ? 'Signing In...' : 'Admin Login'}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>

            {error && (
              <Alert className="mt-4 border-red-200 bg-red-50">
                <AlertDescription className="text-red-700">
                  {error}
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        <div className="text-center mt-6 text-sm text-orange-600">
          <p>Default admin credentials: admin / admin123</p>
        </div>
      </div>
    </div>
  )
}

