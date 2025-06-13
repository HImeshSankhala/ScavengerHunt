import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { LoginPage } from './components/LoginPage'
import { HuntPage } from './components/HuntPage'
import { AdminPage } from './components/AdminPage'
import { AuthProvider, useAuth } from './hooks/useAuth'
import './App.css'

function AppContent() {
  const { user, admin, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-orange-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={!user && !admin ? <LoginPage /> : <Navigate to={admin ? "/admin" : "/hunt"} />} 
        />
        <Route 
          path="/admin" 
          element={admin ? <AdminPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/hunt" 
          element={user ? <HuntPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/" 
          element={<Navigate to={user ? "/hunt" : admin ? "/admin" : "/login"} />} 
        />
      </Routes>
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

