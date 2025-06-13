import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { LogOut, Users, Activity, RotateCcw, SkipForward } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'

export function AdminPage() {
  const { admin, logout, apiCall } = useAuth()
  const [users, setUsers] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [usersData, statsData] = await Promise.all([
        apiCall('/admin/users'),
        apiCall('/admin/stats')
      ])
      setUsers(usersData.users)
      setStats(statsData)
    } catch (error) {
      setError('Failed to load admin data')
    } finally {
      setLoading(false)
    }
  }

  const resetUserProgress = async (userId) => {
    try {
      await apiCall(`/admin/user/${userId}/reset`, { method: 'POST' })
      setSuccess('User progress reset successfully')
      loadData() // Reload data
    } catch (error) {
      setError('Failed to reset user progress')
    }
  }

  const skipUserStep = async (userId) => {
    try {
      await apiCall(`/admin/user/${userId}/skip-step`, { method: 'POST' })
      setSuccess('User step skipped successfully')
      loadData() // Reload data
    } catch (error) {
      setError('Failed to skip user step')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading admin dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">Welcome, {admin?.username}</span>
            <Button onClick={logout} variant="outline" size="sm">
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6 space-y-6">
        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center">
                  <Users className="h-8 w-8 text-blue-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Users</p>
                    <p className="text-2xl font-bold">{stats.total_users}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center">
                  <Activity className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Completed Hunts</p>
                    <p className="text-2xl font-bold">{stats.completed_users}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center">
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Success Rate</p>
                    <p className="text-2xl font-bold">{stats.completion_rate}%</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center">
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Scans</p>
                    <p className="text-2xl font-bold">{stats.total_scans}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
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

        {/* Users Table */}
        <Card>
          <CardHeader>
            <CardTitle>User Management</CardTitle>
            <CardDescription>
              Monitor user progress and manage their hunt experience
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {users.map((user) => (
                <div key={user.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <div>
                        <p className="font-medium">{user.email || user.phone}</p>
                        <p className="text-sm text-gray-500">
                          Step {user.current_step} of 13 • {user.progress_percentage}% complete
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <Badge variant={user.completed_count === 13 ? "default" : "secondary"}>
                          {user.completed_count}/13 completed
                        </Badge>
                        {user.revealed_count > 0 && (
                          <Badge variant="outline">
                            {user.revealed_count} revealed
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Button
                      onClick={() => skipUserStep(user.id)}
                      variant="outline"
                      size="sm"
                      disabled={user.completed_count >= 13}
                    >
                      <SkipForward className="h-4 w-4 mr-1" />
                      Skip Step
                    </Button>
                    <Button
                      onClick={() => resetUserProgress(user.id)}
                      variant="outline"
                      size="sm"
                    >
                      <RotateCcw className="h-4 w-4 mr-1" />
                      Reset
                    </Button>
                  </div>
                </div>
              ))}

              {users.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  No users have started the hunt yet.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

