using System;
using System.IO;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace RevitWindowAutomation
{
    public static class LiveHttpServer
    {
        private static HttpListener? _listener;

        // AppMain'in anlık güncel tuttuğu canlı proje hafıza hücresi
        public static Document? LiveDocument { get; set; }

        public static void Start()
        {
            if (_listener != null && _listener.IsListening) return;

            try
            {
                _listener = new HttpListener();
                _listener.Prefixes.Add("http://localhost:8080/");
                _listener.Start();
                Listen();
            }
            catch (Exception) { /* Port çakışmalarını yut */ }
        }

        private static void Listen()
        {
            if (_listener == null) return;

            _listener.BeginGetContext(asyncResult =>
            {
                try
                {
                    HttpListener? l = (HttpListener?)asyncResult.AsyncState;
                    if (l == null) return;

                    HttpListenerContext context = l.EndGetContext(asyncResult);
                    HttpListenerRequest request = context.Request;
                    HttpListenerResponse response = context.Response;

                    if (request.Url != null && request.Url.AbsolutePath == "/get-windows")
                    {
                        string jsonResponse = "[]";
                        Document? doc = LiveDocument;

                        if (doc != null)
                        {
                            FilteredElementCollector collector = new FilteredElementCollector(doc);
                            collector.OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType();

                            var windowData = collector.Cast<FamilyInstance>().Select(w => new
                            {
                                UniqueId = w.UniqueId,
                                Level = (doc.GetElement(w.LevelId) as Level)?.Name ?? "Level Unknown",
                                Type = w.Symbol.Name,
                                Quantity = 1
                            }).ToList();

                            jsonResponse = JsonSerializer.Serialize(windowData);
                        }

                        byte[] buffer = Encoding.UTF8.GetBytes(jsonResponse);
                        response.ContentType = "application/json";
                        response.ContentLength64 = buffer.Length;
                        response.OutputStream.Write(buffer, 0, buffer.Length);
                        response.OutputStream.Close();
                    }

                    Listen(); // Dinleme döngüsünü sürekli açık tut
                }
                catch (Exception) { /* Thread güvenliği */ }
            }, _listener);
        }

        public static void Stop()
        {
            if (_listener != null && _listener.IsListening)
            {
                _listener.Stop();
                _listener.Close();
            }
        }
    }
}
