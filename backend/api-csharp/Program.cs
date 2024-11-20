using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient();

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(builder =>
    {
        builder.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseCors();

app.MapGet("/", async (HttpClient client, string query) =>
{
    var response = await client.GetStringAsync($"http://flask:5000/api/recommendations?query={query}");
    var data = JsonSerializer.Deserialize<object>(response);
    return Results.Json(data);
});

app.Run();