using System;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Events;

namespace RevitWindowAutomation
{
    public class AppMain : IExternalApplication
    {
        public Result OnStartup(UIControlledApplication application)
        {
            // Revit arka planda her boşa düştüğünde (Idling) canlı dokümanı sunucuya besliyoruz
            application.Idling += OnRevitIdling;

            // Arka plan web sunucumuzu başlatıyoruz
            LiveHttpServer.Start();
            return Result.Succeeded;
        }

        private void OnRevitIdling(object sender, IdlingEventArgs e)
        {
            if (sender is UIApplication uiApp)
            {
                // Revit hafızasındaki en güncel, canlı aktif doküman bağlamını sunucuya paslıyoruz
                LiveHttpServer.LiveDocument = uiApp.ActiveUIDocument?.Document;
            }
        }

        public Result OnShutdown(UIControlledApplication application)
        {
            application.Idling -= OnRevitIdling;
            LiveHttpServer.Stop();
            return Result.Succeeded;
        }
    }
}
