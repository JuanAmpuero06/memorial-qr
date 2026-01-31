import { http, HttpResponse } from 'msw';

// La API URL para tests - el frontend usa http://localhost y luego agrega /api/... o /memorials/...
// Por lo que las llamadas van a http://localhost/memorials/ o http://localhost/api/v1/...
const BASE_URL = 'http://localhost';

export const handlers = [
  // Auth handlers
  http.post(`${BASE_URL}/api/v1/auth/register`, async ({ request }) => {
    const body = await request.json();
    if (body.email === 'existente@example.com') {
      return HttpResponse.json(
        { detail: 'El email ya está registrado' },
        { status: 400 }
      );
    }
    return HttpResponse.json(
      { id: 1, email: body.email },
      { status: 201 }
    );
  }),

  http.post(`${BASE_URL}/api/v1/auth/token`, async ({ request }) => {
    const formData = await request.formData();
    const username = formData.get('username');
    const password = formData.get('password');
    
    if (username === 'test@example.com' && password === 'password123') {
      return HttpResponse.json({
        access_token: 'fake-jwt-token',
        token_type: 'bearer',
      });
    }
    return HttpResponse.json(
      { detail: 'Email o contraseña incorrectos' },
      { status: 401 }
    );
  }),

  // User handlers
  http.get(`${BASE_URL}/api/v1/users/me`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({
      id: 1,
      email: 'test@example.com',
    });
  }),

  // Memorial handlers - Legacy (usado por Dashboard)
  http.get(`${BASE_URL}/memorials/`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json([
      {
        id: 1,
        name: 'Juan Pérez',
        slug: 'juan-perez-abc123',
        epitaph: 'Siempre en nuestros corazones',
        bio: 'Una persona maravillosa',
        birth_date: '1950-03-15',
        death_date: '2024-01-20',
        image_filename: null,
        owner_id: 1,
        created_at: '2024-01-21T10:00:00Z',
      },
    ]);
  }),

  // Memorial handlers (API v1)
  http.get(`${BASE_URL}/api/v1/memorials/`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json([
      {
        id: 1,
        name: 'Juan Pérez',
        slug: 'juan-perez-abc123',
        epitaph: 'Siempre en nuestros corazones',
        bio: 'Una persona maravillosa',
        birth_date: '1950-03-15',
        death_date: '2024-01-20',
        image_filename: null,
        owner_id: 1,
        created_at: '2024-01-21T10:00:00Z',
      },
    ]);
  }),

  http.post(`${BASE_URL}/api/v1/memorials/`, async ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    const body = await request.json();
    return HttpResponse.json(
      {
        id: 2,
        name: body.name,
        slug: `${body.name.toLowerCase().replace(/\s/g, '-')}-test123`,
        epitaph: body.epitaph,
        bio: body.bio,
        birth_date: body.birth_date,
        death_date: body.death_date,
        image_filename: null,
        owner_id: 1,
        created_at: new Date().toISOString(),
      },
      { status: 201 }
    );
  }),

  // Public memorial - API v1
  http.get(`${BASE_URL}/api/v1/memorials/public/:slug`, ({ params }) => {
    if (params.slug === 'no-existe') {
      return HttpResponse.json({ detail: 'Memorial no encontrado' }, { status: 404 });
    }
    return HttpResponse.json({
      name: 'Juan Pérez',
      epitaph: 'Siempre en nuestros corazones',
      bio: 'Una persona maravillosa',
      birth_date: '1950-03-15',
      death_date: '2024-01-20',
      image_filename: null,
    });
  }),

  // Public memorial - Legacy (usado por frontend PublicMemorial.jsx)
  http.get(`${BASE_URL}/public/memorials/:slug`, ({ params }) => {
    if (params.slug === 'no-existe') {
      return HttpResponse.json({ detail: 'Memorial no encontrado' }, { status: 404 });
    }
    return HttpResponse.json({
      name: 'Juan Pérez',
      epitaph: 'Siempre en nuestros corazones',
      bio: 'Una persona maravillosa',
      birth_date: '1950-03-15',
      death_date: '2024-01-20',
      image_filename: null,
    });
  }),

  http.put(`${BASE_URL}/api/v1/memorials/:id`, async ({ request, params }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    const body = await request.json();
    return HttpResponse.json({
      id: parseInt(params.id),
      ...body,
      slug: 'juan-perez-abc123',
      owner_id: 1,
      created_at: '2024-01-21T10:00:00Z',
    });
  }),

  // Legacy put memorial
  http.put(`${BASE_URL}/memorials/:id`, async ({ request, params }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    const body = await request.json();
    return HttpResponse.json({
      id: parseInt(params.id),
      ...body,
      slug: 'juan-perez-abc123',
      owner_id: 1,
      created_at: '2024-01-21T10:00:00Z',
    });
  }),

  http.delete(`${BASE_URL}/api/v1/memorials/:id`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({ message: 'Memorial eliminado correctamente' });
  }),

  // Legacy delete memorial
  http.delete(`${BASE_URL}/memorials/:id`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({ message: 'Memorial eliminado correctamente' });
  }),

  // Analytics handlers - API v1
  http.post(`${BASE_URL}/api/v1/analytics/visit/:slug`, () => {
    return HttpResponse.json({ message: 'Visita registrada', memorial_id: 1 });
  }),

  // Analytics handlers - Legacy (usado por frontend)
  http.post(`${BASE_URL}/analytics/visit/:slug`, () => {
    return HttpResponse.json({ message: 'Visita registrada', memorial_id: 1 });
  }),

  http.get(`${BASE_URL}/api/v1/analytics/reactions/:slug`, () => {
    return HttpResponse.json({
      memorial_id: 1,
      counts: { candle: 5, flower: 3, heart: 10, pray: 2, dove: 1 },
      user_reactions: [],
    });
  }),

  // Legacy reactions get
  http.get(`${BASE_URL}/analytics/reactions/:slug`, () => {
    return HttpResponse.json({
      memorial_id: 1,
      counts: { candle: 5, flower: 3, heart: 10, pray: 2, dove: 1 },
      user_reactions: [],
    });
  }),

  http.post(`${BASE_URL}/api/v1/analytics/reactions/:slug`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      action: 'added',
      reaction_type: body.reaction_type,
      counts: { candle: 5, flower: 3, heart: 11, pray: 2, dove: 1 },
      user_reactions: [body.reaction_type],
    });
  }),

  // Legacy reactions post
  http.post(`${BASE_URL}/analytics/reactions/:slug`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      action: 'added',
      reaction_type: body.reaction_type,
      counts: { candle: 5, flower: 3, heart: 11, pray: 2, dove: 1 },
      user_reactions: [body.reaction_type],
    });
  }),

  http.get(`${BASE_URL}/api/v1/analytics/dashboard`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({
      total_memorials: 5,
      total_visits: 150,
      total_reactions: 45,
      visits_by_day: [],
      reactions_by_type: { candle: 10, flower: 8, heart: 15, pray: 7, dove: 5 },
    });
  }),
  
  // Condolences handlers
  http.get(`${BASE_URL}/api/v1/condolences/:slug`, () => {
    return HttpResponse.json({
      items: [
        {
          id: 1,
          author_name: 'María García',
          author_relationship: 'Amiga',
          message: 'Siempre te recordaremos con cariño',
          is_featured: false,
          created_at: '2024-01-25T10:00:00Z',
        },
        {
          id: 2,
          author_name: 'Pedro López',
          author_relationship: 'Vecino',
          message: 'Descansa en paz',
          is_featured: false,
          created_at: '2024-01-24T15:30:00Z',
        },
      ],
      total: 2,
      pending_count: 0,
    });
  }),

  // Condolences manage handler (para propietarios)
  http.get(`${BASE_URL}/api/v1/condolences/manage/:slug`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({
      items: [
        {
          id: 1,
          author_name: 'María García',
          message: 'Siempre te recordaremos con cariño',
          is_approved: true,
          is_featured: false,
          created_at: '2024-01-25T10:00:00Z',
        },
      ],
      total: 1,
      pending_count: 1,
    });
  }),

  http.post(`${BASE_URL}/api/v1/condolences/:slug`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      {
        id: 3,
        author_name: body.author_name,
        author_relationship: body.author_relationship,
        message: body.message,
        is_approved: false,
        is_featured: false,
        created_at: new Date().toISOString(),
      },
      { status: 201 }
    );
  }),

  // Moderation handlers
  http.patch(`${BASE_URL}/api/v1/condolences/:id`, async ({ request, params }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    const body = await request.json();
    return HttpResponse.json({
      id: parseInt(params.id),
      ...body,
    });
  }),

  http.delete(`${BASE_URL}/api/v1/condolences/:id`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({ message: 'Condolencia eliminada' });
  }),

  // Timeline handlers
  http.get(`${BASE_URL}/api/v1/timeline/:memorialId`, ({ params }) => {
    return HttpResponse.json([
      {
        id: 1,
        title: 'Nacimiento',
        description: 'Nació en Madrid',
        event_date: '1950-03-15',
        memorial_id: parseInt(params.memorialId),
      },
    ]);
  }),

  // Gallery handlers
  http.get(`${BASE_URL}/api/v1/gallery/:memorialId`, ({ params }) => {
    return HttpResponse.json([
      {
        id: 1,
        filename: 'photo1.jpg',
        caption: 'Foto de familia',
        memorial_id: parseInt(params.memorialId),
      },
    ]);
  }),
];
