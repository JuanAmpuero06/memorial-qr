import { http, HttpResponse } from 'msw';

const API_URL = 'http://localhost:8000';

export const handlers = [
  // Auth handlers
  http.post(`${API_URL}/api/v1/auth/register`, async ({ request }) => {
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

  http.post(`${API_URL}/api/v1/auth/token`, async ({ request }) => {
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
  http.get(`${API_URL}/api/v1/users/me`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({
      id: 1,
      email: 'test@example.com',
    });
  }),

  // Memorial handlers
  http.get(`${API_URL}/memorials/`, ({ request }) => {
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

  http.post(`${API_URL}/memorials/`, async ({ request }) => {
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

  http.put(`${API_URL}/memorials/:id`, async ({ request, params }) => {
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

  http.delete(`${API_URL}/memorials/:id`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }
    return HttpResponse.json({ message: 'Memorial eliminado correctamente' });
  }),

  // Public memorial
  http.get(`${API_URL}/public/memorials/:slug`, ({ params }) => {
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

  // Analytics handlers
  http.post(`${API_URL}/analytics/visit/:slug`, () => {
    return HttpResponse.json({ message: 'Visita registrada', memorial_id: 1 });
  }),

  http.get(`${API_URL}/analytics/reactions/:slug`, () => {
    return HttpResponse.json({
      memorial_id: 1,
      counts: { candle: 5, flower: 3, heart: 10, pray: 2, dove: 1 },
      user_reactions: [],
    });
  }),

  http.post(`${API_URL}/analytics/reactions/:slug`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      action: 'added',
      reaction_type: body.reaction_type,
      counts: { candle: 5, flower: 3, heart: 11, pray: 2, dove: 1 },
      user_reactions: [body.reaction_type],
    });
  }),

  http.get(`${API_URL}/api/v1/analytics/dashboard`, ({ request }) => {
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
];
