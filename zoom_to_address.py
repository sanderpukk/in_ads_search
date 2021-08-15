from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QTabWidget
from PyQt5.QtCore import QUrl, QUrlQuery, pyqtSignal, QEventLoop, QCoreApplication

from qgis.core import QgsPointXY, QgsGeometry, QgsRectangle, QgsPoint, QgsWkbTypes, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from qgis.gui import QgsRubberBand


epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

class ZoomToAddress:
    def __init__(self, dialog=None, canvas = None, api_call=None):
        self.dialog = dialog
        self.canvas = canvas
        self.api_call = api_call
        self.crossRb = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.crossRb.setColor(Qt.red)

    def resetRubberbands(self):
        self.crossRb.reset()

    def highlight(self, point):
        currExt = self.canvas.extent()

        leftPt = QgsPoint(currExt.xMinimum(), point.y())
        rightPt = QgsPoint(currExt.xMaximum(), point.y())

        topPt = QgsPoint(point.x(), currExt.yMaximum())
        bottomPt = QgsPoint(point.x(), currExt.yMinimum())

        horizLine = QgsGeometry.fromPolyline([leftPt, rightPt])
        vertLine = QgsGeometry.fromPolyline([topPt, bottomPt])

        self.crossRb.reset(QgsWkbTypes.LineGeometry)
        self.crossRb.addGeometry(horizLine, None)
        self.crossRb.addGeometry(vertLine, None)

        QTimer.singleShot(1700, self.resetRubberbands)

    def zoomTo(self, src_crs, lat, lon):
        canvas_crs = self.canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(src_crs, canvas_crs, QgsProject.instance())
        x, y = transform.transform(float(lon), float(lat))

        rect = QgsRectangle(x, y, x, y)
        self.canvas.setExtent(rect)

        pt = QgsPointXY(x, y)
        self.highlight(pt)
        self.canvas.refresh()
        return pt

    def zoomToCoordinates(self):
        keyAddress = self.dialog.response_list.currentItem().text()
        if keyAddress != 'No match found':
            full_response = self.api_call.search_dictionary[keyAddress]
            lest_x = full_response['viitepunkt_y']
            lest_y = full_response['viitepunkt_x']
            self.zoomTo(QgsCoordinateReferenceSystem("EPSG:3301"), lest_x, lest_y)

